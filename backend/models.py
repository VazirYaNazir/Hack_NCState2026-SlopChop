from pydantic import BaseModel
from typing import Optional

# --- DATA MODELS ---
class PostData(BaseModel):
    id: str
    username: str
    image_url: str
    caption: str
    likes: int
    risk_score: int = 0
    ai_image_probability: float = 0.0
    flag: str = "Analyzing"

class LocationData(BaseModel):
    latitude: float
    longitude: float
