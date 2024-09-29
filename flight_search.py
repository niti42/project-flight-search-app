import os
from dotenv import load_dotenv
import requests
load_dotenv()


AMADEUS_BASE_URL = "https://test.api.amadeus.com"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self) -> None:
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
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        headers = {
            'Authorization': f'Bearer {self._token}'
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
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        city_data = response.json()
        try:
            return city_data['data'][0]['iataCode']

        except (IndexError, KeyError, TypeError) as e:
            print(
                f"Error! No IATA code found for {city}. Exception: {type(e).__name__}")
            return "N/A"

        except requests.exceptions.RequestException as e:
            print(f"Request failed for {city}. Exception: {type(e).__name__}")
            return "N/A"


if __name__ == "__main__":
    search = FlightSearch()
    iata = search.get_iata_code("Paris")
    print("IATA code: ", iata)
