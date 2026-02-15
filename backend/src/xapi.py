import tweepy as tw
from dotenv import load_dotenv
import os

load_dotenv()
xapi: str = os.getenv("XAPI")
client = tw.Client(bearer_token=xapi)

# We need to first get the location of the user,
# using latitude and longitude, coordinates.

