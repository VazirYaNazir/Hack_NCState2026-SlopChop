from pydantic import BaseModel
from typing import List, Optional
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import torch.nn.functional as F

MODELS = {
    "openai-roberta": {"name": "openai-community/roberta-base-openai-detector", "weight": 1.0},
    "chatgpt-roberta": {"name": "Hello-SimpleAI/chatgpt-detector-roberta", "weight": 0.7}
}

loaded_models = {k: {"tokenizer": AutoTokenizer.from_pretrained(v["name"]),
                     "model": AutoModelForSequenceClassification.from_pretrained(v["name"]),
                     "weight": v["weight"]}
                 for k, v in MODELS.items()}

def get_ai_percentage(text):
    total, weight_sum = 0, 0
    for info in loaded_models.values():
        inputs = info["tokenizer"](text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            logits = info["model"](**inputs).logits
            if logits.shape[-1] == 2:
                ai_prob = F.softmax(logits, dim=-1)[0][1].item() * 100
            else:
                ai_prob = torch.sigmoid(logits[0][0]).item() * 100
        total += ai_prob * info["weight"]
        weight_sum += info["weight"]
    return round(total / weight_sum, 1)


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
def scan_post_caption(input_data: str) -> int:
    total, weight_sum = 0, 0
    for info in loaded_models.values():
        inputs = info["tokenizer"](input_data, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            logits = info["model"](**inputs).logits
            if logits.shape[-1] == 2:
                ai_prob = F.softmax(logits, dim=-1)[0][1].item() * 100
            else:
                ai_prob = torch.sigmoid(logits[0][0]).item() * 100
        total += ai_prob * info["weight"]
        weight_sum += info["weight"]
    return round(total / weight_sum, 1)
