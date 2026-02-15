import json 
import fastapi


app = fastapi.FastAPI()

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