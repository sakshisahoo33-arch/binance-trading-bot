# Binance Futures Testnet Trading Bot

## Overview
A CLI-based trading bot built in Python for placing orders on Binance Futures Testnet, featuring robust error handling and a structured logging system.

## Features
- Market and Limit orders
- Stop-Market and Stop-Limit orders
- CLI input using `argparse`
- Input validation with descriptive error messages
- Structured logging (console + rotating file)
- Granular error handling (network, auth, API, validation)

## Project Structure
```
trading_bot/
├── cli.py          # Entry point — argument parsing & orchestration
├── client.py       # Binance HTTP client (signing, requests, retries)
├── orders.py       # Order builder & submission logic
├── validators.py   # Input validation helpers
├── logger.py       # Logging configuration
└── README.md
```

## Setup

### 1. Install dependencies
```bash
pip install requests
```

### 2. Configure API keys
Create a `.env` file or export environment variables:
```bash
export BINANCE_API_KEY=your_testnet_api_key
export BINANCE_API_SECRET=your_testnet_api_secret
```
> Get your testnet keys at: https://testnet.binancefuture.com

## How to Run

**Market Order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Limit Order:**
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 70000
```

**Stop-Market Order:**
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 60000
```

**Stop-Limit Order:**
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP --quantity 0.001 --price 59500 --stop-price 60000
```

## Logging
Logs are written to both the console and a rotating file (`logs/bot.log`).

| Level | When |
|-------|------|
| `INFO` | Order placed, responses received |
| `WARNING` | Retryable issues, unexpected fields |
| `ERROR` | API errors, validation failures |
| `DEBUG` | Full request/response payloads (use `--debug` flag) |

Enable debug mode:
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --debug
```

## Error Handling
| Error Type | Class | Description |
|---|---|---|
| Network/timeout | `BinanceNetworkError` | No connectivity or request timed out |
| Auth failure | `BinanceAuthError` | Invalid or missing API key/secret |
| API rejection | `BinanceAPIError` | Binance returned a non-2xx error code |
| Bad input | `ValidationError` | Invalid symbol, side, quantity, etc. |

## Challenges Faced
- Binance Testnet secret key is only shown once at generation — must be copied immediately
- Timestamp synchronisation between local machine and Binance servers can cause signature errors; resolved using `recvWindow`

## What I Learned
- CLI application design with `argparse`
- Modular Python architecture (client, orders, validators, logger)
- HMAC-SHA256 request signing for authenticated REST APIs
- Layered error handling and structured logging best practices
