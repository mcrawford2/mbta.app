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

## Date: 2026-04-18

**What I asked AI to do:**
- AI helped with creating the Flask app, when connecting the python file, html file, and css file. 
- while organizing the new files into different folders, I asked AI "update any code after folder changes" so that all references were correct
- I often asked AI to explain specific lines, especially if it was written by the AI, to ensure I had an understanding of how it all interacts
- While testing user inputs, I often received the message: This page isn’t working. If the problem continues, contact the site owner. HTTP ERROR 405. I asked AI to help resolve this

**What I didn't understand in the generated code:**
- I didn't understand how the python file and HTML file were interacting
- I didn't understand the line 'place= "Boston Common"'
- I didn't understand {%...%} in the results.html file
- Why AI generated two HTML files, rather than just using the one I had created


**What I learned:**
- 
- 'place = "Boston Common"' is a hardcoded test input for the main() function later. It allows the script to do one quick lookup without asking for user input, but only needs to run when main() is called.
- {% ... %} runs template statements, like if/else, loops, and block endings. {{ ... }} prints a value into the page.
- There are two HTML files because the app has two separate views: index.html is the home page with the form, and results.html is the results page shown after the POST request. This also keeps the form simple for users and helps with understanding errors. 
- the error: HTTP ERROR 405 was due to mbta.py only allowing POST, rather than both POST and GET. 
