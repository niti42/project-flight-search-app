# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

import requests
import json
from pprint import pprint

sheet_data_get_url = r'https://api.sheety.co/bb7b4db22c7482feb06a54c51f8e5bf2/flightDeals/prices'


def get_sheet_data():
    response = requests.get(sheet_data_get_url)
    sheet_data = response.json()
    return sheet_data


def check_if_field_empty(table, column):
    for row in sheet_data:
        if row.get(column) == '':
            continue
        else:
            return False
    return True


with open('flight-deals-prices.json', 'r') as f:
    data = json.load(f)

sheet_data = data.get('prices')

is_iatacode_empty = check_if_field_empty(sheet_data, 'iataCode')
print(is_iatacode_empty)

# check if iataCode column is empth
