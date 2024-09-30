import requests
import os
from dotenv import load_dotenv
from flight_search import FlightSearch

search = FlightSearch()

load_dotenv()


SHEETY_PRICES_ENDPOINT = 'https://api.sheety.co/bb7b4db22c7482feb06a54c51f8e5bf2/flightDeals/prices'


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheet_data_url = SHEETY_PRICES_ENDPOINT
        self._authorization = os.getenv('Authorization')
        self.headers = {
            "Authorization": self._authorization
        }
        self.destination_data = {}

    def get_destination_data(self):
        try:
            response = requests.get(self.sheet_data_url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            self.destination_data = data.get("prices")
            return self.destination_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")

    def update_destination_code(self, row_id, destination_code):
        edited_row = {
            "price": {
                "iataCode": destination_code
            }
        }
        update_url = f'{self.sheet_data_url}/{row_id}'
        try:
            response = requests.put(
                url=update_url, json=edited_row, headers=self.headers)
            response.raise_for_status()
            print(
                f"Row {row_id} updated successfully. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error updating row {row_id}: {e}")


if __name__ == "__main__":
    row_edit = {"price": {"city": "Frankfurt",
                          "iataCode": "TESTING", "lowestPrice": 42, "id": 3}}

    row_num = 3
    update_url = f'https://api.sheety.co/bb7b4db22c7482feb06a54c51f8e5bf2/flightDeals/prices/{row_num}'

    response = requests.put(url=update_url, json=row_edit)
    print(response)
