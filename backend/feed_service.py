import ai_engine
import random

# --- THE MOCK DATASET ---
def get_mock_feed():
    return [
        {
            "id": "demo_scam_1",
            "username": "elon_giveaway_official",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlSP-QgB_POFLe9i3pdDlCabp4BYp0kfnIxA&s", 
            "caption": "URGENT: Doubling all BTC sent to my wallet! Link in bio! Spots sell out fast! 🚀🔴 #crypto #giveaway #tesla",
            "likes": 5210,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending"
        },
        {
            "id": "demo_safe_1",
            "username": "charles_leclerc",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-T4WIUWFWLMoqYTEPmnuB_6BGx2vzylAK7A&s",
            "caption": "Lots of work done over the last 3 days. Few days to analyse everything and we go again next week!",
            "likes": 616375,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending"
        },
        {
            "id": "demo_scam_2",
            "username": "microsoft_support_team",
            "image_url": "https://learn-attachment.microsoft.com/api/attachments/2099d340-79fa-4ac1-89e3-b38115071bbd?platform=QnA", 
            "caption": "Your account has been locked due to suspicious activity. Click the link in our bio to verify your identity or your account will be deleted in 24 hours. 🔒",
            "likes": 122843,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending"
        },
        {
            "id": "demo_safe_2",
            "username": "charlesschwab",
            "image_url": "https://learn-attachment.microsoft.com/api/attachments/2099d340-79fa-4ac1-89e3-b38115071bbd?platform=QnA",
            "caption": "Leveling up to 70k FOLLOWERS! We're thankful for each and every one of you for following along with us.",
            "likes": 161,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending"
        },
        {
            "id": "demo_scam_3",
            "username": "amazon_giveaway",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9mKWuNz3EHZ29V2YvBKVENdcmJjQS8Z8M5Q&s", 
            "caption": "AMAZON PRIME DAY GIVEAWAY! 🎉🎁 Win a $500 Amazon Gift Card! To enter: 1) Follow us 2) Like this post 3) Tag 3 friends in the comments. Hurry, ends soon! #AmazonPrimeDay #Giveaway",
            "likes": 9248,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending"
        },
        {
            "id": "demo_safe_3",
            "username": "travel_weekly",
            "image_url": "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1",
            "caption": "Top 10 destinations to visit in Switzerland this winter. 🏔️🇨🇭 #travel #wanderlust",
            "likes": 8943,
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
    _inject_hero_post(feed, "microsoft_support_team", 1)

    analyzed_feed = []
    
    for post in feed:
        try:
            print(f"Processing post: {post['id']}...")
            
            # 1. Run Text Analysis
            risk_score = ai_engine.scan_post_caption(post["caption"])
            
            # 2. Run Image Analysis
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
            print(f"AI Error on {post['id']}: {e}")
            post['risk_score'] = -1
            post['flag'] = "AI Error"
            
        analyzed_feed.append(post)

    return analyzed_feed

def _inject_hero_post(feed_list, hero_id, target_index=1):
    """
    Shuffles the feed but ensures the 'hero' post is at a specific index.
    """
    # Find the hero
    hero_post = next((item for item in feed_list if item["id"] == hero_id), None)
    
    # Get everyone else
    others = [item for item in feed_list if item["id"] != hero_id]
    
    # Shuffle the rest
    random.shuffle(others)
    
    # Insert Hero back in (if it exists)
    if hero_post:
        # Ensure index isn't out of bounds
        insert_idx = min(target_index, len(others))
        others.insert(insert_idx, hero_post)
        
    return others