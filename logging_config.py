"""
Logging configuration for the Binance Futures Trading Bot.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "trading_bot.log")


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Configure structured logging to both console and a rotating log file.

    Args:
        log_level: Logging level string (DEBUG, INFO, WARNING, ERROR).

    Returns:
        Configured root logger.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    # Rotating file handler (5 MB per file, keep 3 backups)
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(numeric_level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING)  # Only warnings+ to console

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return root_logger
