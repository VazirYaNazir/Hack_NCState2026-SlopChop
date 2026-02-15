import tweepy as tw
from dotenv import load_dotenv
import json
import os

load_dotenv()
xapi: str = os.getenv("XAPI")
client = tw.Client(bearer_token=xapi)

# We need to first get the location of the user,
# using latitude and longitude, coordinates.

lat_state = 35.7833592
long_state = -78.670738

trends = client.closest_trends(lat=lat_state, long=long_state)