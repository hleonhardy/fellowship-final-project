# Sun Setup

Sun Setup uses the altitudes and amounts of clouds given by aviation weather
forecasts in order to generate a prediction about the sunset for any given
location as well as a recommendation of any nearby location that has a higher
rated sunset.
In order to get the nearby forecasts, Sun Setup queries a database of airports to find all the airports within a default of 50km of the user which can then be used to make a bulk API request to CheckWX to get the forecasts.

### What makes a good sunset?

The ideal sunset for this project was one that had mid level clouds taking up roughly half the sky. This is what will give us the nice pinks, reds, and oranges.
A clear sky is considered to have a neutral sunset and a completely overcast sky is bad.

### Why use aviation weather forecasts?

I chose to use the forecasts from aviation weather reports because of how specific the cloud information was. A normal forecast might say "overcast" or "partly cloudy" but an aviation weather forecast specifies the amount and altitude of the clouds. For example, it might say that we have 1/8 of the sky filled with clouds at 2000ft. 
With this information I was able to generate a more accurate prediction of the sunset.

### Tech Stack

Python, Javascript, HTML/CSS, Flask, Bootstrap, jQuery, Jinja, 
Flask-SQLAlchemy, GeoAlchemy, PostgreSQL, PostGIS,
datetime, timezonefinder, pytz,
Google Maps API, CheckWX API, Sunrise-Sunset API

### Features

* uses JS Geolocation function to get browser coordinates
* Can also type in LAT/LNG, Google maps autocomplete address, or choose
 from favorite locations (if user is logged in) on the advanced search page.
* Also on advanced search page can change the distance that you're querying
* A user can also log in to add favorite locations and upload photos

### Example Storyline

We'll start with the homepage:

![Alt text](/screenshots/home.png?raw=true "Sun Setup Home")

By clicking the "click here" to get started button, we use JavaScript's geolocation function to get my location (San Francisco):

![Alt text](/screenshots/sf.png?raw=true "My location")

Let's say I have a friend in Missoula, MT. I can type in her location into the nav bar to get a prediction for Missoula:

![Alt text](/screenshots/m1.png?raw=true "Too Cloudy")

It's too cloudy. Drat. What if we change the distance in which we are searching from 50km to 500km? There might be a better prediction a little farther away.

![Alt text](/screenshots/adv.png?raw=true "Advanced Search")

Aha! There is a perfect sunset prediction only 235 km away! I hope my friend has a car...

![Alt text](/screenshots/m2.png?raw=true "Perfect Prediction")

Here you can see all the locations checked by the program (represented by airplanes on the map)

![Alt text](/screenshots/m4.png?raw=true "All Airports")




