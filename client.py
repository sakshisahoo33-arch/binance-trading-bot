"""
Low-level Binance Futures Testnet REST API client.

Handles authentication (HMAC-SHA256 signature), request/response logging,
retry logic, and error normalisation.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import time
from typing import Any
from urllib.parse import urlencode

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

BASE_URL = "https://testnet.binancefuture.com"
RECV_WINDOW = 5000  # milliseconds


class BinanceAPIError(RuntimeError):
    """Wraps a Binance API error response."""

    def __init__(self, code: int, msg: str) -> None:
        self.code = code
        self.msg = msg
        super().__init__(f"Binance API error {code}: {msg}")


class BinanceClient:
    """
    Thin wrapper around the Binance Futures Testnet REST API.

    Args:
        api_key: Testnet API key.
        api_secret: Testnet API secret.
        base_url: Base URL for the testnet (default: https://testnet.binancefuture.com).
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = BASE_URL,
    ) -> None:
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = base_url.rstrip("/")
        self._session = self._build_session()

    # ------------------------------------------------------------------ #
    #  Public helpers                                                       #
    # ------------------------------------------------------------------ #

    def get_account_info(self) -> dict[str, Any]:
        """Return current futures account information."""
        return self._signed_get("/fapi/v2/account")

    def get_exchange_info(self) -> dict[str, Any]:
        """Return exchange info (symbol filters, precision, etc.)."""
        return self._get("/fapi/v1/exchangeInfo")

    def place_order(self, params: dict[str, Any]) -> dict[str, Any]:
        """
        Submit a new order.

        Args:
            params: Mapping of Binance order parameters (symbol, side,
                    type, quantity, price, …).

        Returns:
            Binance order response dict.
        """
        logger.info("Placing order | params=%s", params)
        response = self._signed_post("/fapi/v1/order", params)
        logger.info("Order response | %s", response)
        return response

    # ------------------------------------------------------------------ #
    #  Private HTTP helpers                                                 #
    # ------------------------------------------------------------------ #

    def _build_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update({"X-MBX-APIKEY": self._api_key})
        # Auto-retry on transient network errors (not on 4xx / 5xx)
        retry = Retry(
            total=3,
            backoff_factor=0.5,
            allowed_methods=["GET", "POST", "DELETE"],
            status_forcelist=[502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def _sign(self, query_string: str) -> str:
        return hmac.new(
            self._api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _signed_get(self, path: str, params: dict | None = None) -> dict[str, Any]:
        params = params or {}
        params["timestamp"] = int(time.time() * 1000)
        params["recvWindow"] = RECV_WINDOW
        query = urlencode(params)
        params["signature"] = self._sign(query)
        url = f"{self._base_url}{path}"
        logger.debug("GET %s | params=%s", url, params)
        resp = self._session.get(url, params=params, timeout=10)
        return self._handle_response(resp)

    def _signed_post(self, path: str, params: dict | None = None) -> dict[str, Any]:
        params = params or {}
        params["timestamp"] = int(time.time() * 1000)
        params["recvWindow"] = RECV_WINDOW
        query = urlencode(params)
        params["signature"] = self._sign(query)
        url = f"{self._base_url}{path}"
        logger.debug("POST %s | params=%s", url, params)
        resp = self._session.post(url, params=params, timeout=10)
        return self._handle_response(resp)

    @staticmethod
    def _handle_response(resp: requests.Response) -> dict[str, Any]:
        logger.debug("HTTP %s | body=%s", resp.status_code, resp.text[:500])
        try:
            data = resp.json()
        except ValueError:
            resp.raise_for_status()
            raise RuntimeError(f"Non-JSON response: {resp.text[:200]}")

        if isinstance(data, dict) and "code" in data and data["code"] != 200:
            raise BinanceAPIError(data["code"], data.get("msg", "Unknown error"))

        resp.raise_for_status()
        return data
