from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ai_engine
import feed_service
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

@app.get("/api/feed")
def get_feed():
    return feed_service.generate_analyzed_feed()
    
    

@app.post("/api/submit-location")
async def receive_location(loc: LocationData):
    print(f"RECEIVED COORDINATES: {loc.latitude}, {loc.longitude}")
    # Here you can add logic to store the location or use it elsewhere.
    return {
        "message": "Location received",
        "latitude": loc.latitude,
        "longitude": loc.longitude
    }

@app.get("/api/get-image")
def getImage():
    """
    This is the endpoint for 
    sending the twitter images to the frontend.
    """
    return {"status": "not implemented yet"}

@app.get("/api/get-news")
def getNews():
    """
    This is the endpoint for 
    sending the twitter news to the frontend.
    """
    return {"status": "not implemented yet"}