# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

import requests
import json
from pprint import pprint
from flight_search import FlightSearch
from data_manager import DataManager
from copy import deepcopy
from flight_search import FlightSearch

flight_search = FlightSearch()


data_manager = DataManager()
sheet_data = data_manager.get_destination_data()

for index, row in enumerate(sheet_data):
    if row.get('iataCode') == '':
        iata_code = flight_search.get_iata_code(
            row.get('city'))
        data_manager.destination_data[index]['iataCode'] = iata_code
        data_manager.update_destination_code(
            row_id=row.get('id'), destination_code=iata_code)
