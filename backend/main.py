from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ai_engine
import feed_service
from backend.src.googleapi import coords_to_geo
from backend.src.xapi import get_posts_from_trends_as_real_tweets as get_trending_posts
from models import LocationData, PostData

app = FastAPI()

# --- MIDDLEWARE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MAIN ENDPOINT ---
@app.get("/api")
async def root():
    return {"message": "Hello World"}

# --- FEED ENDPOINT ---
@app.get("/api/feed")
def get_feed():
    return feed_service.generate_analyzed_feed()
    
# --- LOCATION BASED TWITTER TRENDS ENDPOINT ---
@app.post("/api/submit-location")
async def receive_location(loc: LocationData):
    print(f"RECEIVED COORDINATES: {loc.latitude}, {loc.longitude}")
    try:
        post_info = get_trending_posts(coords_to_geo(loc.latitude, loc.longitude), 10, 1)
    except Exception as e:
        print(f"Error occurred while fetching trending posts: {e}")
        return {"error": str(e)}
    #Returns the list of trending posts in a LIST of JSONs format, similar to other api endpoints.
    return post_info["posts"]