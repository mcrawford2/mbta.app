import json
import os
from urllib.error import HTTPError
from urllib.parse import quote_plus #encodes place names for use in URLs
from urllib.parse import urlencode #turns a dictionary of query parameters into a URL-encoded string, helps send longitude and latitude
from urllib.request import urlopen #sends HTTP requests to Mapbox API
from flask import Flask, redirect, render_template, request, url_for #Flask allows the creation of web applications. render_template is used to render HTML templates, and request is used to access form data sent by the user.

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

	if not data.get("features"):
		raise ValueError("No matching place was found.")

	longitude, latitude = data["features"][0]["center"]
	return latitude, longitude


def get_nearest_stop(latitude: float, longitude: float):
	'''Returns the nearest MBTA stop name and whether it is wheelchair accessible.'''
	url = f"https://api-v3.mbta.com/stops?{urlencode({'sort': 'distance', 'filter[latitude]': latitude, 'filter[longitude]': longitude, 'page[limit]': 1})}"
	with urlopen(url) as response:
		data = json.loads(response.read().decode("utf-8")) #converts raw data string returned by urlopen into a regular string, and json.loads() breaks down that string into a python dictionary. Parsing makes it a manipulatable object.

	if not data.get("data"):
		raise ValueError("No nearby MBTA stops were found.")

	stop = data["data"][0]["attributes"] #API returns the first/nearest stop from the list with [0]. Then we access the "attributes" key to get the details of that stop.
	return {
		"name": stop["name"],
		"wheelchair_accessible": stop.get("wheelchair_boarding") == 1,
		"latitude": stop.get("latitude"),
		"longitude": stop.get("longitude"),
	}


def find_stop_nearby(place_name: str, mapbox_token: str):
	'''Find the nearest MBTA stop to a place name. Combines get_location and get_nearest_stop.'''
	latitude, longitude = get_location(place_name, mapbox_token) #
	stop = get_nearest_stop(latitude, longitude)
	return {
		"place_latitude": latitude,
		"place_longitude": longitude,
		"stop": stop,
	}

#web

app = Flask( #uses folders to create flask app
	__name__,
	template_folder=os.path.join("helloflask", "templates"),
	static_folder=os.path.join("helloflask", "static"),
)


@app.route("/", methods=["GET", "POST"])
def home():
	'''Renders the home page and handles form submissions.'''
	if request.method == "GET":
		return render_template("index.html")

	place_name = request.form.get("place_name", "").strip()
	mapbox_token = os.getenv("MAPBOX_API_KEY")

	if not mapbox_token:
		return render_template(
			"results.html",
			place_name=place_name,
			error="MAPBOX_API_KEY was not found in your .env file or environment.",
		)

	if not place_name:
		return render_template(
			"results.html",
			place_name=place_name,
			error="Please enter a place name.",
		)

	try:
		result = find_stop_nearby(place_name, mapbox_token)
	except HTTPError as e:
		return render_template(
			"results.html",
			place_name=place_name,
			error=f"API error: {e.code} {e.reason}",
		)
	except ValueError as e:
		return render_template(
			"results.html",
			place_name=place_name,
			error=str(e),
		)
	except Exception as e:
		return render_template(
			"results.html",
			place_name=place_name,
			error=f"Unexpected error: {e}",
		)

	return render_template(
		"results.html",
		place_name=place_name,
		stop_name=result["stop"]["name"],
		wheelchair_accessible=result["stop"]["wheelchair_accessible"],
		place_latitude=result["place_latitude"],
		place_longitude=result["place_longitude"],
		stop_latitude=result["stop"]["latitude"],
		stop_longitude=result["stop"]["longitude"],
		mapbox_public_token=mapbox_token,
	)


@app.route("/index.html", methods=["GET", "POST"])
def index_html():
	'''Compatibility route for browser testing from the template file.'''
	return home()


@app.route("/results", methods=["GET", "POST"])
def results():
	'''Handles form submissions and renders the results page.'''
	place_name = request.values.get("place_name", "").strip()
	if request.method == "GET" and not place_name:
		return redirect(url_for("home"))

	mapbox_token = os.getenv("MAPBOX_API_KEY")

	if not mapbox_token:
		return render_template(
			"results.html",
			place_name=place_name,
			error="MAPBOX_API_KEY was not found in your .env file or environment.",
		)

	if not place_name:
		return render_template(
			"results.html",
			place_name=place_name,
			error="Please enter a place name.",
		)

	try:
		result = find_stop_nearby(place_name, mapbox_token)
	except HTTPError as e:
		return render_template(
			"results.html",
			place_name=place_name,
			error=f"API error: {e.code} {e.reason}",
		)
	except ValueError as e:
		return render_template(
			"results.html",
			place_name=place_name,
			error=str(e),
		)
	except Exception as e:
		return render_template(
			"results.html",
			place_name=place_name,
			error=f"Unexpected error: {e}",
		)

	return render_template(
		"results.html",
		place_name=place_name,
		stop_name=result["stop"]["name"],
		wheelchair_accessible=result["stop"]["wheelchair_accessible"],
		place_latitude=result["place_latitude"],
		place_longitude=result["place_longitude"],
		stop_latitude=result["stop"]["latitude"],
		stop_longitude=result["stop"]["longitude"],
		mapbox_public_token=mapbox_token,
	)


@app.route("/results.html", methods=["GET", "POST"])
def results_html():
	'''Compatibility route for browser testing from the template file.'''
	return results()


def main():
	mapbox_token = os.getenv("MAPBOX_API_KEY")
	if not mapbox_token:
		print("Error: MAPBOX_API_KEY not found in .env file or environment.")
		return
	
	place = "Boston Common"
	
	try:
		print(f"Finding nearest stop to {place}...")
		result = find_stop_nearby(place, mapbox_token)
		
		print(f"Stop: {result['stop']['name']}")
		print(f"Wheelchair accessible: {result['stop']['wheelchair_accessible']}")
	except HTTPError as e:
		print(f"API Error: {e.code} {e.reason}")
	except ValueError as e:
		print(f"Error: {e}")
	except Exception as e:
		print(f"Error: {e}")


if __name__ == "__main__":
	app.run(debug=True)

