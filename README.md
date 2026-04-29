# Binance Futures Testnet Trading Bot

## Overview
This is a CLI-based trading bot built in Python that allows users to place orders on Binance Futures Testnet.

## Features
- Market and Limit orders
- Stop-Market and Stop-Limit orders
- CLI input using argparse
- Input validation
- Logging system
- Error handling

## How to Run

Market Order:
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

Limit Order:
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 70000

## Challenges Faced
- Faced issue with Binance testnet API key generation (secret key not visible)
- Due to this, API execution could not be fully tested but later on did it anyhow 

## What I Learned
- CLI-based application design
- Modular coding (client, orders, validators)
- Handling API errors and validation
- This is how its worked 
