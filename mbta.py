import json
import os
from urllib.error import HTTPError
from urllib.parse import quote_plus #encodes place names for use in URLs
from urllib.parse import urlencode #turns a dictionary of query parameters into a URL-encoded string, helps send longitude and latitude
from urllib.request import urlopen #sends HTTP requests to Mapbox API

#for loading API keys, necessary because of many previous errors with API keys. This tries to use the dotenv library to load environment variables from a .env file, but if that library isn't available, it manually reads the .env file and setting environment variables.
try:
	from dotenv import load_dotenv
	env_path = os.path.join(os.path.dirname(__file__), ".env")
	load_dotenv(env_path)
except ImportError:
	# Fallback: manually read .env file
	env_path = os.path.join(os.path.dirname(__file__), ".env")
	if os.path.exists(env_path):
		with open(env_path) as f:
			for line in f:
				line = line.strip()
				if line and not line.startswith("#") and "=" in line:
					key, value = line.split("=", 1)
					os.environ[key.strip()] = value.strip()


def get_location(place_name: str, access_token: str): #access_token is ID for Mapbox authentication
	'''Finds the latitude and longitude of a place using the Mapbox Geocoding API.'''
	query = quote_plus(place_name) #quote_plus is a URL encoding function
	url = (
		f"https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json"
		f"?access_token={access_token}&limit=1"
	)

	with urlopen(url) as response:
		data = json.loads(response.read().decode("utf-8"))

	longitude, latitude = data["features"][0]["center"]
	return latitude, longitude


def get_nearest_stop(latitude: float, longitude: float):
	'''Returns the nearest MBTA stop name and whether it is wheelchair accessible.'''
	url = f"https://api-v3.mbta.com/stops?{urlencode({'sort': 'distance', 'filter[latitude]': latitude, 'filter[longitude]': longitude, 'page[limit]': 1})}"
	with urlopen(url) as response:
		data = json.loads(response.read().decode("utf-8")) #converts raw data string returned by urlopen into a regular string, and json.loads() breaks down that string into a python dictionary. Parsing makes it a manipulatable object.

	stop = data["data"][0]["attributes"] #API returns the first/nearest stop from the list with [0]. Then we access the "attributes" key to get the details of that stop.
	return stop["name"], stop.get("wheelchair_boarding") == 1


def find_stop_nearby(place_name: str, mapbox_token: str):
	'''Find the nearest MBTA stop to a place name. Combines get_location and get_nearest_stop.'''
	latitude, longitude = get_location(place_name, mapbox_token) #
	return get_nearest_stop(latitude, longitude)


def main():
	mapbox_token = os.getenv("MAPBOX_API_KEY")
	if not mapbox_token:
		print("Error: MAPBOX_API_KEY not found in .env file or environment.")
		return
	
	place = "Boston Common"
	
	try:
		print(f"Finding nearest stop to {place}...")
		stop_name, wheelchair_accessible = find_stop_nearby(place, mapbox_token)
		
		print(f"Stop: {stop_name}")
		print(f"Wheelchair accessible: {wheelchair_accessible}")
	except HTTPError as e:
		print(f"API Error: {e.code} {e.reason}")
	except Exception as e:
		print(f"Error: {e}")


if __name__ == "__main__":
	main()

