import requests
import json

start_location = "Boston, MA"
end_location = "New York, NY"
api_key = ""

url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_location}&destination={end_location}&mode=driving&key={api_key}"

response = requests.get(url)
data = json.loads(response.text)

# if data is an error message:
# print(data["error_message"])

if data["status"] != "OK":
    print("Error: " + data["error_message"])
    exit()

route = data["routes"][0]["legs"][0]["steps"]

# render the route

for step in route:
    print(step["html_instructions"])
    print("Distance: " + step["distance"]["text"])
    print("Duration: " + step["duration"]["text"])
    print()

