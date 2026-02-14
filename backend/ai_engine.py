from pydantic import BaseModel
from typing import List, Optional

# Data format for the post
class ModelInput(BaseModel):
    post_id: str
    caption: str
    image_url: str
    # Add extra fields if he needs them (e.g., user_biography)

# 2. THE OUTPUT FORMAT (Data format for the AI's response)
class ModelOutput(BaseModel):
    risk_score: int  # 0-100
    flags: List[str] # ["Crypto Scam", "Deepfake"]
    debug_info: Optional[str] = None

# 3. Hugging Face Workspace
def scan_post(input_data: ModelInput) -> ModelOutput:
    """
    Teammate: Implement your Hugging Face model here.
    """
    print(f"AI Scanning Post: {input_data.post_id}")
    # Example:
    # risk = my_hugging_face_model.predict(input_data.caption)
    
    # For now, keep the mock logic until hugging face is set up:
    text = input_data.caption.lower()
    score = 10
    detected_flags = []
    
    if "giveaway" in text or "btc" in text:
        score = 95
        detected_flags.append("Crypto Scam")
    
    if "urgent" in text:
        score += 20
        detected_flags.append("Pressure Language")
        
    # --- Hugging Face Code Ends Here ---
    
    return ModelOutput(
        risk_score=min(score, 100), 
        flags=detected_flags,
        debug_info="Analyzed via Heuristic Engine v1"
    )