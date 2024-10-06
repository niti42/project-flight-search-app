from pprint import pprint
from flight_data import FlightData
from flight_search import FlightSearch
from data_manager import DataManager
from copy import deepcopy
from flight_search import FlightSearch
from datetime import datetime, timedelta
import time
import asyncio

from notifications import send_email, send_telegram_message

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
    for idx, day in enumerate(range(5)):
        future_day = timestamp_today + timedelta(day)
        future_day_str = future_day.strftime("%Y-%m-%d")
        return_day = future_day + timedelta(1)
        return_day_str = return_day.strftime("%Y-%m-%d")
        try:
            all_flights = flight_search.get_all_flights(
                origin_loc_code="LON",
                destination_loc_code=row.get('iataCode'),
                departure_date=future_day_str,
                return_date=return_day_str,
            )

            # print(f"Getting flights for {city}...")
            flight_data.find_cheapest_flight(all_flights)
            # print(f"{city}:{flight_data.price}")
            prices_60d.append((idx, flight_data.price, flight_data))
        except Exception as e:
            print(f"Error Fetching data: {e}")
            continue

    time.sleep(2)
    prices_60d.sort(key=lambda x: x[1])

    historical_low = row.get('lowestPrice')

    if prices_60d[0][1] < historical_low:
        print("60d lowest: ", prices_60d[0][1],
              ',', "Prev Lowest", historical_low)

        price = prices_60d[0][2].price
        departure_iata = prices_60d[0][2].origin_airport
        arrival_iata = prices_60d[0][2].destination_airport
        outbound_date = prices_60d[0][2].out_date
        inbound_date = prices_60d[0][2].return_date

        message = f"""
Only £{price} to fly from {departure_iata} to {arrival_iata} 
on {outbound_date} until {inbound_date}"""

        print(message)

        # send_email(subject="Low Price alert!",
        #            message=message,
        #            to_email='nithishkr136@yahoo.com')

        # Send telegram notification
        asyncio.run(send_telegram_message(message))

    else:
        print(f"No Cheapest flight found for {city}")
