import json 
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LocationData(BaseModel):
    latitude: float
    longitude: float
    accuracy: Optional[float] = None

@app.post("/api/location")
def receive_location(location: LocationData):
    """Receive geolocation from frontend"""
    print(f"Received location: {location.latitude}, {location.longitude}")
    return {
        "message": "Location received",
        "latitude": location.latitude,
        "longitude": location.longitude
    }

@app.get("/api")
async def root():
    return {"message": "Hello World"}

@app.get("/api/lagLong")
def lagLong(lat: float, long: float):
    """We use this for the 
    geolocation of twitter news"""
    
    return {"latitude": lat, "longitude": long}

@app.get("/api/getimage")
def getImage():
    """
    This is the endpoint for 
    sending the twitter images to the frontend.
    """
    return

@app.get("/api/getnews")
def getNews():
    """
    This is the endpoint for 
    sending the twitter news to the frontend.
    """
    return