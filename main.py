# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from pprint import pprint
from flight_data import FlightData
from flight_search import FlightSearch
from data_manager import DataManager
from copy import deepcopy
from flight_search import FlightSearch
from datetime import datetime, timedelta
MONTHS = 6


def update_iata_code_in_sheet(sheet_data):
    for index, row in enumerate(sheet_data):
        if row.get('iataCode') == '':
            iata_code = flight_search.get_iata_code(
                row.get('city'))
            data_manager.destination_data[index]['iataCode'] = iata_code
            data_manager.update_destination_code(
                row_id=row.get('id'), destination_code=iata_code)


flight_search = FlightSearch()
data_manager = DataManager()
flight_data = FlightData()


sheet_data = data_manager.get_destination_data()
update_iata_code_in_sheet(sheet_data)

timestamp_today = datetime.now()
today_date = timestamp_today.strftime("%Y-%m-%d")

for row in sheet_data:
    city = row.get('city')

    prices_60d = []
    for idx, day in enumerate(range(MONTHS*30)):
        future_day = timestamp_today + timedelta(day)
        future_day = future_day.strftime("%Y-%m-%d")
        return_day = future_day + timedelta(5)
        all_flights = flight_search.get_all_flights(
            origin_loc_code="LON",
            destination_loc_code=row.get('iataCode'),
            departure_date=future_day,
            return_date=return_day,
        )

        # print(f"Getting flights for {city}...")
        flight_data.find_cheapest_flight(all_flights)
        # print(f"{city}:{flight_data.price}")
        prices_60d.append((idx, flight_data.price, flight_data))


# search for the flight prices from London (LON) to all the destinations in the Google Sheet.
# looking only for non stop flights that leave anytime between tomorrow and in 6 months (6x30days) time
# round trips for 1 adult. currency of the price we get back should be in GBP.


# understand the problem
# the script should check for prices once every day.
# assume 1 week roundtrip duration (5 days)
# For a given day do this:

# get prices for the destination for the next 60 days
# Find if price for any day is lower than the historical low price listed in the table for the respective country
# If you do get a flight meeting the prev cond. then get its details
