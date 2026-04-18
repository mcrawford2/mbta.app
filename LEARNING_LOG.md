## Date: 2026-04-17

**What I asked AI to do:**
- I asked AI for help with using urllib.parse. 
- I asked AI to help make the get_nearest_stop function safer, and it reported back that "It now: checks that latitude and longitude are valid numbers in range, calls the MBTA stops API with a timeout, handles HTTP and network errors, returns the nearest stop name plus wheelchair accessibility as True, False, or None if unknown"

**What I didn't understand in the generated code:**
- I didn't understand certain functions of urllib.parse, such as quote_plus
- I didn't know that type hints, like place_name: str, could be used in parameters
- I didn't understand why "utf-8" was appearing in the get_nearest_stop function because I am used to seeing that only in an HTML context


**What I learned:**
- I have a better understanding of what it takes to write code for turning text into safe URLs
- I learned a new feature of parameters, which does not force the type at runtime, but it helps with readability and catching errors.
- I learned that "utf-8" is in the python script to convert raw data from the APIs HTTP response into readable text