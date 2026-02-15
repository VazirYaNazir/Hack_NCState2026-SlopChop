import instaloader
import pickle
import os
import json

# --- CONFIGURATION ---
SESSION_FILENAME = "backend/session-quackpromax" 

def inspect_feed_data():
    print("🔍 INITIALIZING DATA INSPECTOR...")
    print("-" * 50)

    # 1. LOAD SESSION
    L = instaloader.Instaloader()
    try:
        if not os.path.exists(SESSION_FILENAME):
            print(f"❌ Error: Session file '{SESSION_FILENAME}' not found.")
            return

        with open(SESSION_FILENAME, 'rb') as f:
            data = pickle.load(f)
            if isinstance(data, dict):
                L.context._session.cookies.update(data)
            else:
                L.load_session_from_file("quackpromax", filename=SESSION_FILENAME)
        print(f"✅ Session Loaded for: {L.context.username}")

    except Exception as e:
        print(f"❌ Session Load Failed: {e}")
        return

    # 2. FETCH LIVE FEED
    print("🔄 Fetching live feed from Instagram...")
    try:
        # Get the actual home feed
        posts = L.get_feed_posts()
        
        count = 0
        print("\n📢 --- DATA SENT TO AI MODEL ---")
        
        for post in posts:
            if count >= 3: break # Only show top 3 posts
            
            # 3. CONSTRUCT THE EXACT DATA PACKET
            # This mimics the 'ModelInput' class we defined earlier
            ai_data_packet = {
                "post_id": post.shortcode,
                "caption": post.caption if post.caption else "[NO CAPTION]",
                "image_url": post.url,
                "metadata": {
                    "username": post.owner_username,
                    "likes": post.likes,
                    "timestamp": str(post.date_local)
                }
            }
            
            # 4. PRETTY PRINT THE DATA
            print(f"\n📄 POST #{count + 1} ({post.owner_username})")
            print(f"   ID: {ai_data_packet['post_id']}")
            print(f"   Caption Preview: \"{ai_data_packet['caption'][:100]}...\"")
            print(f"   Image URL: {ai_data_packet['image_url'][:50]}...")
            
            # DUMP RAW JSON (So you can copy-paste to your teammate)
            print("   ⬇️ RAW JSON FOR AI:")
            print(json.dumps(ai_data_packet, indent=4))
            print("-" * 50)
            
            count += 1
            
    except Exception as e:
        print(f"❌ Error fetching feed: {e}")

if __name__ == "__main__":
    inspect_feed_data()