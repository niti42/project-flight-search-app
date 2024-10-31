from flight_data import FlightData
from flight_search import FlightSearch
from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
import time
import asyncio
import math

from notification_manager import NotificationManager
from notifications import send_email, send_telegram_message

from dotenv import load_dotenv
import os


load_dotenv()
# Initialize the event loop at the start
loop = asyncio.get_event_loop()

TGRAM_BOT_TOKEN = os.getenv('flight_deal_finder_bot_token')
TGRAM_BOT_USERNAME = os.getenv('flight_deal_finder_bot_user_name')
CHAT_ID = os.getenv('flight_deal_finder_bot_chat_id')

my_email = os.getenv("my_email")
password = os.getenv("password")

MONTHS = (5/30)  # for testing: days/30
RETURN_AFTER_DAYS = 5


def update_iata_code_in_sheet(sheet_data):
    for index, row in enumerate(sheet_data):
        if row.get('iataCode') == '':
            iata_code = flight_search.get_iata_code(
                row.get('city'))
            data_manager.destination_data[index]['iataCode'] = iata_code
            data_manager.update_destination_code(
                row_id=row.get('id'), destination_code=iata_code)


def check_flights_60d(row, non_stop="true"):
    prices_60d = []
    # here, need to get for 60 days i.e months*60. current val = 5 for testing
    for idx, day in enumerate(range(math.ceil(MONTHS*30))):
        future_day = timestamp_today + timedelta(day)
        future_day_str = future_day.strftime("%Y-%m-%d")
        return_day = future_day + timedelta(RETURN_AFTER_DAYS)
        return_day_str = return_day.strftime("%Y-%m-%d")
        try:
            all_flights = flight_search.get_all_flights(
                origin_loc_code="LON",
                destination_loc_code=row.get('iataCode'),
                departure_date=future_day_str,
                return_date=return_day_str,
                non_stop=non_stop
            )
            flight_data.find_cheapest_flight(all_flights)
            prices_60d.append((idx, flight_data.price, flight_data))
        except Exception as e:
            print(f"Error Fetching data: {e}")
            continue

    return prices_60d


flight_search = FlightSearch()
data_manager = DataManager()
flight_data = FlightData()
notification_manager = NotificationManager(
    telegram_token=TGRAM_BOT_TOKEN, telegram_chat_id=CHAT_ID, email_address=my_email, email_password=password)


sheet_data = data_manager.get_destination_data()
update_iata_code_in_sheet(sheet_data)
customer_data = data_manager.get_customer_emails()
customer_emails = [c.get('whatIsYourEmail?') for c in customer_data]

timestamp_today = datetime.now()
today_date = timestamp_today.strftime("%Y-%m-%d")

for row in sheet_data:
    city = row.get('city')
    prices_60d = check_flights_60d(row)
    time.sleep(2)

    prices_60d = [item for item in prices_60d if item[1] != 'N/A']

    if not prices_60d:
        print(f"Checking flights with stops for {city}")
        prices_60d = check_flights_60d(row, non_stop="false")
        prices_60d = [item for item in prices_60d if item[1] != 'N/A']

    if not prices_60d:
        print(f"No valid prices found for {city} even with stopovers.")
        continue  # Skip to the next iteration

    prices_60d.sort(key=lambda x: x[1])
    historical_low = float(row.get('lowestPrice', 'inf'))

    if prices_60d[0][1] < historical_low:

        stops = prices_60d[0][2].stops
        price = prices_60d[0][2].price
        departure_iata = prices_60d[0][2].origin_airport
        arrival_iata = prices_60d[0][2].stops[-1] if len(
            stops) > 1 else prices_60d[0][2].destination_airport
        outbound_date = prices_60d[0][2].out_date
        inbound_date = prices_60d[0][2].return_date

        print("city: ", city, "\n")

        message = f"""
Only £{price} to fly from {departure_iata} to {arrival_iata} 
on {outbound_date} until {inbound_date}, stops: {",".join(stops)}"""

        print(message)
        print('\n')

        # uncomment if you want to send telegram messages
        # print(message)
        # loop.run_until_complete(
        #     notification_manager.send_telegram_message(message))

        # for email in customer_emails:
        #     notification_manager.send_email(
        #         subject="Low Price alert!", message=message, to_email=email
        #     )
    else:
        print(f"No Cheapest flight found for {city}")
loop.close()
