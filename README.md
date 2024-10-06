# Flight Deals Finder

## Overview

Flight Deals Finder tracks flight prices from London (LON) to multiple destinations. It checks prices over a 60-day window and notifies the user when a lower-than-historical price is found, using either email or a Telegram bot.

## Features

- **IATA Code Updates**: Automatically updates IATA codes for destination cities in Google Sheets if they are missing.
- **Price Fetching**: Fetches flight data for the next 5 days for each destination.
- **Price Comparison**: Compares current flight prices with historical lowest prices.
- **Notifications**: Sends alerts via Telegram when a lower price is found.

## Prerequisites

- Python 3.x
- Required Python packages:
  - `python-telegram-bot`
  - `requests`
  - `pprint`
  - Other dependencies from the project's modules: `FlightData`, `FlightSearch`, `DataManager`

## Setup

1. Install dependencies:

   ```bash
   pip install python-telegram-bot requests


   ```

2. Set up a Google Sheet to manage destination data.
3. Get a bot token from Telegram's BotFather.

## Usage

The script retrieves the lowest flight prices and sends notifications if a price is lower than the historical low. You can configure the script to notify via:

- Email (via the send_email function)
- Telegram (via the send_telegram_message function)

## Customization

- Adjust the number of days to check prices by modifying MONTHS = 6.
- Modify how the IATA codes and prices are stored and updated via the DataManager class.
