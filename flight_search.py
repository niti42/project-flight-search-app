import os
from dotenv import load_dotenv
import requests
load_dotenv()


AMADEUS_BASE_URL = "https://test.api.amadeus.com"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["AMADEUS_API_SECRET"]
        self._token = self._get_new_token()

    def _get_new_token(self):
        url = f"{AMADEUS_BASE_URL}/v1/security/oauth2/token"

        # url = "https://test.api.amadeus.com/v1/security/oauth2/token"

        # note: payload can also be sent as a dictionary. this is the body
        payload = f"grant_type=client_credentials&client_id={self._api_key}&client_secret={self._api_secret}"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("access_token")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")

    def get_iata_code(self, city):
        url = f"{AMADEUS_BASE_URL}/v1/reference-data/locations/cities"

        headers = {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        params = {
            "keyword": city,
            "max": 2,
            "include": "AIRPORTS"
        }
        try:
            return self.request_iata_code(url, headers, params, city)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")

    def request_iata_code(self, url, headers, params, city):
        try:
            response = requests.get(url=url, headers=headers, params=params)
            response.raise_for_status()
            city_data = response.json()
            return city_data['data'][0]['iataCode']

        except (IndexError, KeyError, TypeError) as e:
            print(
                f"Error! No IATA code found for {city}. Exception: {type(e).__name__}")
            return "N/A"

        except requests.exceptions.RequestException as e:
            print(f"Request failed for {city}. Exception: {type(e).__name__}")
            return "N/A"

    def get_all_flights(self, origin_loc_code, destination_loc_code, departure_date, return_date, adults=1, currency_code='GBP', non_stop='true'):
        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        headers = {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        params = {
            "originLocationCode": origin_loc_code,
            "destinationLocationCode": destination_loc_code,
            "departureDate": departure_date,
            "returnDate": return_date,
            "adults": adults,
            "currencyCode": currency_code,
            "nonStop": non_stop
        }

        try:
            response = requests.get(url=url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(
                f"Request failed for {destination_loc_code}. Exception: {type(e).__name__}")
            return None


if __name__ == "__main__":
    from pprint import pprint
    from flight_data import FlightData
    search = FlightSearch()
    flight_data = FlightData()
    all_flights = search.get_all_flights(
        origin_loc_code="LON",
        destination_loc_code="PAR",
        departure_date="2024-10-01",
        return_date="2024-10-06",
    )

    flight_data.find_cheapest_flight(all_flights)

    print(flight_data.price)
