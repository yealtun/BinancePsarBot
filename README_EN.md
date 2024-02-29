# Trading Bot with Binance API

## Overview

This repository contains a simple Python trading bot that utilizes the Binance API for executing trades based on Parabolic SAR (PSAR) indicator signals. The bot is designed for trading cryptocurrency futures.

## Prerequisites

Before using the bot, make sure you have the following:

- Python 3 installed
- Required Python packages installed (`ccxt`, `pandas`, `ta`, `winsound`)
- Binance API key and secret (get them from your Binance account)

## Configuration

1. Open `config.py` and fill in your Binance API key (`apiKey`) and secret (`secretKey`).
2. Optionally, provide email details in `config.py` if you want to receive notifications.
   - `mailAddress`: Your email address
   - `mailAddress2`: Another email address (optional)
   - `password`: Email password (use an app-specific password for security)

## Usage

1. Run `strategy.py`.
2. Enter the symbol name (e.g., BTC, ETH), leverage, and time frame when prompted.
3. The bot will continuously monitor PSAR signals and execute trades accordingly.

## PSAR Strategy

- **Long Entry:** Buy when the close price crosses above the PSAR.
- **Short Entry:** Sell when the close price crosses below the PSAR.
- **Stop-loss and Take-profit:** Dynamic adjustments based on market conditions.

## Notifications

- If email details are provided, the bot will send notifications for trade entries and exits.

## Important Notes

- Use this bot at your own risk. Understand the code and trading strategies before deploying.
- Ensure proper risk management and configure leverage cautiously.

## Issues

If you encounter issues or have suggestions, please create a GitHub issue.

## Disclaimer

This trading bot is for educational purposes only. It is not financial advice. Use it responsibly and at your own risk.
