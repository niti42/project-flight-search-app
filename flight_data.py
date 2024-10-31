from flight_search import FlightSearch

flight_search = FlightSearch()


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, price="N/A", origin_airport="N/A", destination_airport="N/A", out_date="N/A", return_date="N/A"):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.num_stops = 0
        self.stops = []

    def find_cheapest_flight(self, all_flights):
        if all_flights_data := all_flights.get('data'):
            all_trips = [
                (idx, float(trip.get('price').get('total')))
                for idx, trip in enumerate(all_flights_data)
            ]
            # sort the tuple in ascending order. first val is the lowest price trip
            all_trips.sort(key=lambda x: x[1])

            # get the index of the lowest price data in all_flights data
            lowest_price_idx = all_trips[0][0]
            lowest_price = all_trips[0][1]

            # selects the trip with lowest price
            lowest_price_trip = all_flights_data[lowest_price_idx]

            self.price = lowest_price
            self.origin_airport = lowest_price_trip.get('source')
            self.destination_airport = lowest_price_trip.get('itineraries')[0].get('segments')[
                -1].get('arrival').get('iataCode')
            self.out_date = lowest_price_trip.get('itineraries')[0].get('segments')[
                0].get('departure').get('at')
            self.return_date = lowest_price_trip.get('itineraries')[1].get('segments')[
                0].get('departure').get('at')
            self.num_stops = len(lowest_price_trip.get(
                "itineraries")[0].get("segments"))
            self.stops = [s.get("arrival").get("iataCode") for s in lowest_price_trip.get(
                "itineraries")[0].get("segments")]
