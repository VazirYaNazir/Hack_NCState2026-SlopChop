import ai_engine

# --- THE MOCK DATASET ---
def get_mock_feed():
    return [
        {
            "id": "demo_scam_1",
            "username": "elon_giveaway_official",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlSP-QgB_POFLe9i3pdDlCabp4BYp0kfnIxA&s", 
            "caption": "URGENT: Doubling all BTC sent to my wallet! Link in bio! Spots sell out fast! 🚀🔴 #crypto #giveaway #tesla",
            "likes": 5200,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending"
        },
        {
            "id": "demo_safe_1",
            "username": "tech_crunch",
            "image_url": "https://images.unsplash.com/photo-1519389950473-47ba0277781c",
            "caption": "Breaking: OpenAI releases GPT-5 preview. The new model is 10x faster and safer. #ai #tech #future",
            "likes": 15400,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending"
        },
        {
            "id": "demo_scam_2",
            "username": "instagram_support_team",
            "image_url": "https://placehold.co/600x600/orange/white?text=Acct+Locked", 
            "caption": "Your account has been locked due to suspicious activity. Click the link in our bio to verify your identity or your account will be deleted in 24 hours. 🔒",
            "likes": 45,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending"
        },
        {
            "id": "demo_safe_2",
            "username": "travel_weekly",
            "image_url": "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1",
            "caption": "Top 10 destinations to visit in Switzerland this winter. 🏔️🇨🇭 #travel #wanderlust",
            "likes": 8900,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending"
        }
    ]

# --- THE LOGIC ---
def generate_analyzed_feed():
    """
    Fetches the mock feed and runs the AI engine on each post.
    """
    feed = get_mock_feed()
    analyzed_feed = []
    
    for post in feed:
        try:
            print(f"Processing post: {post['id']}...")
            
            # 1. Run Text Analysis
            risk_score = ai_engine.scan_post_caption(post["caption"])
            
            # 2. Run Image Analysis (Optional)
            ai_prob = ai_engine.get_ai_image_probability(post["image_url"])
            
            # 3. Update Post Data
            post['risk_score'] = risk_score
            post['ai_image_probability'] = ai_prob

            # 4. Set Flags based on score
            if risk_score > 75:
                post['flag'] = "SCAM DETECTED"
            elif risk_score > 40:
                post['flag'] = "Suspicious"
            else:
                post['flag'] = "Safe"
                
        except Exception as e:
            print(f"⚠️ AI Error on {post['id']}: {e}")
            post['risk_score'] = -1
            post['flag'] = "AI Error"
            
        analyzed_feed.append(post)

    return analyzed_feed