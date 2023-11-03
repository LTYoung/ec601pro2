import googlemaps
from datetime import datetime
import requests

api_key = ''

# Set up the Google Maps API client
gmaps = googlemaps.Client(key=api_key)

# Take input for the starting and ending locations of the route
start_location = input("Enter the starting location: ")
end_location = input("Enter the ending location: ")

# Use the Google Maps API to get the directions for the route
now = datetime.now()
directions_result = gmaps.directions(start_location, end_location, mode="driving", departure_time=now)

# Extract the coordinates of the route from the directions
coordinates = []
for step in directions_result[0]['legs'][0]['steps']:
    coordinates.append((step['start_location']['lat'], step['start_location']['lng']))

# Use the Google Places API to search for EV charging stations of the specified type (CCS, Tesla) within a certain radius of each coordinate along the route

ev_stations = []
for coord in coordinates:
    lat, lng = coord
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type=charging_station&keyword=CCS|Tesla&key={api_key}"
    response = requests.get(url)
    results = response.json()['results']
    for result in results:
        ev_stations.append(result['name'])

# Display each station with its address, plug type, and number of available plugs
for station in ev_stations:
    url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={station}&inputtype=textquery&fields=formatted_address,name,opening_hours,geometry&key={api_key}"
    response = requests.get(url)
    results = response.json()['candidates']
    for result in results:
        # only print each item if it exist (if no opening hours, don't print it)
        print(result['name'])
        print(result['formatted_address'])
        print(result['opening_hours']['weekday_text'])
        print(result['geometry']['location'])
        print()
