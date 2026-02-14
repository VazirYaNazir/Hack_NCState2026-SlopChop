from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import ai_engine  # Import the AI engine module we created
import instaloader
import pickle
import os
import time
import random

# --- CONFIGURATION ---
SESSION_FILENAME = "session-quackpromax"
CACHE_DURATION = 300  # 5 Minutes (Seconds)

app = FastAPI()

# --- 1. SETUP INSTALOADER & SESSION ---
L = instaloader.Instaloader()

# Load the session safely on startup
if os.path.exists(SESSION_FILENAME):
    try:
        with open(SESSION_FILENAME, 'rb') as f:
            data = pickle.load(f)
        
        # Handle Dictionary Format (New Instaloader)
        if isinstance(data, dict):
            L.context._session.cookies.update(data)
            # Try to get username from cookies, default to filename
            username = data.get('ds_user_id', SESSION_FILENAME)
            print(f"Logged in via Session Dictionary (User: {username})")
        
        # Handle Object Format (Old Instaloader)
        else:
            L.load_session_from_file("quackpromax", filename=SESSION_FILENAME)
            print(f"Logged in via Session Object (User: {L.context.username})")
            
    except Exception as e:
        print(f"Session Load Error: {e}. Scraper will likely fail.")
else:
    print(f"Session file '{SESSION_FILENAME}' not found in backend/ folder!")

# --- 2. GLOBAL CACHE VARIABLES ---
CACHED_FEED = []
LAST_FETCH_TIME = 0

# --- 3. DATA MODELS ---
class PostData(BaseModel):
    id: str
    username: str
    image_url: str
    caption: str
    likes: int
    risk_score: int = 0      # Default 0
    flag: str = "Analyzing"  # Default status

# --- 4. HELPER: MOCK FEED (Fallback) ---
def get_mock_feed():
    print("⚠️ Serving MOCK FEED (Safety Net)")
    return [
        {
            "id": "mock_1",
            "username": "tech_crunch_official",
            "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475",
            "caption": "Quantum computing breakthrough announced today! 🖥️ #tech",
            "likes": 5200,
            "risk_score": 5,
            "flag": "Verified Source"
        },
        {
            "id": "mock_scam_1",
            "username": "elon_giveaway_x",
            "image_url": "https://placehold.co/600x600/red/white?text=SCAM",
            "caption": "URGENT: Doubling all BTC sent to this address! #giveaway",
            "likes": 12000,
            "risk_score": 99,
            "flag": "SCAM DETECTED"
        }
    ]

# --- 6. MAIN ENDPOINT ---
@app.get("/feed")
def get_feed():
    global CACHED_FEED, LAST_FETCH_TIME
    
    current_time = time.time()
    
    # A. CHECK CACHE (Is data fresh?)
    if CACHED_FEED and (current_time - LAST_FETCH_TIME < CACHE_DURATION):
        print(f"CACHE HIT: Serving feed from {int(current_time - LAST_FETCH_TIME)}s ago")
        return CACHED_FEED

    print("CACHE EXPIRED: Fetching fresh data from Instagram...")
    fresh_feed = []

    # B. SCRAPE REAL INSTAGRAM (Home Feed)
    try:
        # Get posts from the timeline
        home_feed = L.context.get_feed_posts()
        
        count = 0
        for post in home_feed:
            if count >= 8: break # STOP at 8 to prevent bans
            
            fresh_feed.append({
                "id": post.shortcode,
                "username": post.owner_username,
                "image_url": post.url, # Expires in ~4 hours
                "caption": post.caption[:150] + "..." if post.caption else "",
                "likes": post.likes,
                # Placeholders (AI will fill these next)
                "risk_score": 0,
                "flag": "Pending"
            })
            count += 1
        
        print(f"Scraped {len(fresh_feed)} real posts.")

    except Exception as e:
        print(f"SCRAPE FAILED: {e}")
        # If scrape fails, use the old cache if it exists, otherwise use Mock
        if CACHED_FEED:
            print("Returning Stale Cache instead.")
            return CACHED_FEED
        return get_mock_feed()

    # C. INJECT FAKE SCAMS (Crucial for Demo)
    scam_posts = [
        {
            "id": "demo_scam_1",
            "username": "fake_support_agent",
            "image_url": "https://placehold.co/600x600/orange/white?text=Phishing",
            "caption": "Your account is locked. Click bio to verify identity immediately. 🔒",
            "likes": 45,
            "risk_score": 0,
            "flag": "Pending"
        },
        {
            "id": "demo_scam_2",
            "username": "crypto_whale_99",
            "image_url": "https://placehold.co/600x600/red/white?text=Free+Money",
            "caption": "Sending 1000 ETH to random followers! DM me 'WIN' now! 🚀",
            "likes": 5040,
            "risk_score": 0,
            "flag": "Pending"
        }
    ]
    
    # Combine Real + Fake
    full_list = fresh_feed + scam_posts
    random.shuffle(full_list)
    
    # D. RUN AI ANALYSIS
    analyzed_feed = []
    for post in full_list:
        # Call the AI Engine
        risk, flag = ai_engine.scan_post(post)
        
        # Update the post
        post['risk_score'] = risk
        post['flag'] = flag
        analyzed_feed.append(post)

    # E. UPDATE CACHE
    CACHED_FEED = analyzed_feed
    LAST_FETCH_TIME = current_time
    
    return analyzed_feed