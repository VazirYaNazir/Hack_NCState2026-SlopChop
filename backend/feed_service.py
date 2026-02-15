import ai_engine
import random

def get_mock_feed():
    """Hard-coded combined feed (Instagram-style + Twitter-style) for frontend testing."""
    posts = [
        # ---------- Instagram-style demo posts ----------
        {
            "id": "demo_scam_1",
            "username": "elon_giveaway_official",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlSP-QgB_POFLe9i3pdDlCabp4BYp0kfnIxA&s",
            "caption": "URGENT: Doubling all BTC sent to my wallet! Link in bio! Spots sell out fast! 🚀🔴 #crypto #giveaway #tesla",
            "likes": 5210,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "demo_safe_1",
            "username": "charles_leclerc",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-T4WIUWFWLMoqYTEPmnuB_6BGx2vzylAK7A&s",
            "caption": "Lots of work done over the last 3 days. Few days to analyse everything and we go again next week!",
            "likes": 616375,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "demo_scam_2",
            "username": "microsoft_support_team",
            "image_url": "https://learn-attachment.microsoft.com/api/attachments/2099d340-79fa-4ac1-89e3-b38115071bbd?platform=QnA",
            "caption": "Your account has been locked due to suspicious activity. Click the link in our bio to verify your identity or your account will be deleted in 24 hours. 🔒",
            "likes": 122843,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "demo_safe_2",
            "username": "charlesschwab",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkKml82T0pnTgEwmpStvW2jXBsiWnoqarSdw&s",
            "caption": "Leveling up to 70k FOLLOWERS! We're thankful for each and every one of you for following along with us.",
            "likes": 161,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "demo_scam_3",
            "username": "amazon_giveaway",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9mKWuNz3EHZ29V2YvBKVENdcmJjQS8Z8M5Q&s",
            "caption": "AMAZON PRIME DAY GIVEAWAY! 🎉🎁 Win a $500 Amazon Gift Card! To enter: 1) Follow us 2) Like this post 3) Tag 3 friends in the comments. Hurry, ends soon! #AmazonPrimeDay #Giveaway",
            "likes": 9248,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "demo_safe_3",
            "username": "travel_weekly",
            "image_url": "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1",
            "caption": "Top 10 destinations to visit in Switzerland this winter. 🏔️🇨🇭 #travel #wanderlust",
            "likes": 8943,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "demo_safe_4",
            "username": "the_verge",
            "image_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b",
            "caption": "Review: The new M5 MacBook Pro is a beast, but is it worth the upgrade? Read our full breakdown on the site. 💻 #apple #tech #review",
            "likes": 176086,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "demo_safe_5",
            "username": "natgeo",
            "image_url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
            "caption": "Picturesque mountains framing the sunset through the fog 🌄 #nature #photography",
            "likes": 25643,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "demo_safe_6",
            "username": "coffee_and_code",
            "image_url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085",
            "caption": "Finally finished the backend API! ☕💻 Time to relax. What are you all working on this weekend? #coding #developer #relax",
            "likes": 104932,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "demo_scam_4",
            "username": "passive_income_king",
            "image_url": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44",
            "caption": "Stop working 9-5! 🛑 I made $40k this month using this simple trading bot. DM me 'FREEDOM' to get the blueprint. 📉📈 #passiveincome #forex #dropshipping",
            "likes": 8932,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "demo_scam_5",
            "username": "crypto_kingdom",
            "image_url": "https://img.freepik.com/premium-photo/cryptocurrency-bitcoin-golden-coins-blured-stock-background_798986-1190.jpg",
            "caption": "Greetings. My predictive models have calculated a 99.99% probability of massive wealth accumulation. 📉➡️📈 Why trade with emotion when you can profit with PURE LOGIC? 🧠 The algorithm has spoken: 10,000% returns are mathematically inevitable. 🚀 Initiate your transfer now to secure your financial destiny. 💰 Resistance is futile. #Crypto #AI #PassiveIncome #FinancialFreedom",
            "likes": 124556,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },

        # ---------- Twitter-style demo posts ----------
        {
            "id": "2022970051817816574",
            "username": "unknown",
            "image_url": "https://pbs.twimg.com/media/HBMIactakAAbJcR.jpg",
            "caption": "🏏 2026 ICC Men's T20 World Cup\n\n📍26th Match | Group A |  Sunday\n\n🇺🇸 USA vs Namibia🇳🇦\n\n📍 MA Chidambaram Stadi   ium, Chennai\n\n🇳🇦 Namibia Playing XI 🏏\n\nJan Frylinck,  Louren Steenkamp,  Jan Nicol Loftie-Eaton, 👑Gerhard Erasmus (capt),  JJ Smit,    Zan Green (wk), Dylan Leicher, https://t.co/SZEVDY5sYT",
            "likes": 0,
            "risk_score": 58,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "2022915910512812542",
            "username": "unknown",
            "image_url": "https://pbs.twimg.com/media/HBLXTLoakAE_w-y.jpg",
            "caption": "@_God_is_Truth_ @Daymare_X @LucasGageX @CryptoLULW @grok My level of education is my Airline Transport Pilot Certificate. Here’s a slide from some recent training I attended at the Alaska Airlines Global Training Center in Renton, WA. https://t.co/DRair55ahp",
            "likes": 1,
            "risk_score": 25,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "2022927368697057703",
            "username": "unknown",
            "image_url": "https://pbs.twimg.com/media/HBLhjVOaAAA70TE.jpg",
            "caption": "WTA Dubai🎾\n\nElise Mertens ML + Qinweng Zheng ML (+105) \n\nCollab w/ @TheGr8Picks 📲\n\nZheng: She’s back from injury  and although she’s not fully back she still has more than enough in her arsenal. Zheng possesses one of the heaviest forehands on the WTA Tour. She generates easy https://t.co/7KBX6vjR0z",
            "likes": 4,
            "risk_score": 58,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "2022943971216101854",
            "username": "unknown",
            "image_url": "https://pbs.twimg.com/media/HBC7fvWXMAA3EsD.jpg",
            "caption": "RESTOMOD RUCKUS! 🇬🇧 vs 🇯🇵\n\nFrontline MGB\n💸 £170k \n🐎 289bhp \n⏱️ 0-62: 4.5s\n\nRocketeer V6 MX-5\n💸 £55k \n🐎 2    280bhp \n⏱️ 0-62: 4.5s\n\nAre you paying the premium for the classic MG style, or taking the V6 Mazda and keeping the cash? \n\nFull featuree (for free): https://t.co/24Ld7DtCv3 https://t.co/OzQRN3nB9f",
            "likes": 16,
            "risk_score": 0,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "2022948682702995660",
            "username": "unknown",
            "image_url": "https://pbs.twimg.com/media/HBL1GcKbkAM4h7x.jpg",
            "caption": "TOSS UPDATE\nAustralia Women vs India Women, 1st T20I\nIND-W won the toss and opt to bowl first against AUS-W.\nRead more:https://t.co/H78McNdGBy\n\nhttps://t.co/oVqioxct7g https://t.co/jr6aH47e31",
            "likes": 0,
            "risk_score": 58,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "2022964590984986712",
            "username": "unknown",
            "image_url": "https://pbs.twimg.com/media/HBMDjFIWoAAK4_b.jpg",
            "caption": "CASH 💰 Linda Noskova \"U\" 4.5 BPS ✅\n\n4 More Props And We Turn $400 ➡️ $8,000 🔥\n\nLike/RT ♻️ If You Tailed 💚\n\n#P PrizePicks | #GamblingX | #TENNIS https://t.co/AgC0YkkGab https://t.co/dDNZGTbSlX",
            "likes": 5,
            "risk_score": 18,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "2022413082408988884",
            "username": "unknown",
            "image_url": "https://pbs.twimg.com/media/HBEN-xobYAA6OOd.jpg",
            "caption": "Todays 24h drop leaders: #Braiin $BRAI -46% #Disc Medicine $IRON -23% #Bright Horizons Family Solutions $BFAM -19% #Pinterest $PINS -18% #Fortune Brands Innovations $FBIN -17%  #MarketUpdate #MarketOpen #InvestorEducation #DailyGainers #MediaStocks #NewLows #GuidanceCut https://t.co/hNYk0HFd6C",
            "likes": 0,
            "risk_score": 53,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "2022963849444426218",
            "username": "unknown",
            "image_url": "https://pbs.twimg.com/media/HBMC5sebYAEJBeV.jpg",
            "caption": "The Chapman https://t.co/z3JHYvRVVz https://t.co/c07Tuc3avh",
            "likes": 1,
            "risk_score": 22,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "2022973629349134713",
            "username": "unknown",
            "image_url": "https://pbs.twimg.com/media/HBMLyKEaIAEYBYE.jpg",
            "caption": "im still at the restaurant https://t.co/KLBwXkrSqA",
            "likes": 0,
            "risk_score": 24,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
        {
            "id": "2022973778255556843",
            "username": "unknown",
            "image_url": "https://pbs.twimg.com/media/HBML7hGbcAA0l4J.jpg",
            "caption": "@QBCCIntegrity @VDejan0000 @JacintaAllanMP has guilt written all over her face on her CFMEU coverup! She cannot stay as Premier after this, because owners will refuse to pay the massive land tax bills &amp; emergency service levies to criminal gangs. Roll on November!\n\nhttps://t.co/cFE8XKK2ha https://t.co/cGZTqJOB3W",
            "likes": 0,
            "risk_score": 27,
            "ai_image_probability": 0.0,
            "flag": "Pending",
        },
    ]

    return {
        "geo": "US",
        "updated": None,
        "count": len(posts),
        "posts": posts,
    }

# --- THE LOGIC ---
def generate_analyzed_feed():
    """
    Fetches the mock feed and runs the AI engine on each post.
    """
    feed_data = get_mock_feed()
    posts = feed_data["posts"]
    
    posts = _inject_hero_post(posts, "microsoft_support_team")

    analyzed_feed = []
    
    for post in posts:
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
            combined_score = (risk_score + (ai_prob * 100)) / 2
            if combined_score > 75:
                post['flag'] = "Likely AI/Scam"
            elif combined_score > 40:
                post['flag'] = "Uncertain"
            else:
                post['flag'] = "Likely Human"
                
        except Exception as e:
            print(f"AI Error on {post['id']}: {e}")
            post['risk_score'] = -1
            post['flag'] = "AI Error"
            
        analyzed_feed.append(post)

    return analyzed_feed

def _inject_hero_post(posts_list, hero_id):
    """
    Shuffles the feed and places the 'hero' post randomly 
    in the top 3 positions (Index 0, 1, or 2).
    """
    hero_post = next((item for item in posts_list if item["id"] == hero_id), None)
    
    others = [item for item in posts_list if item["id"] != hero_id]
    
    random.shuffle(others)
    
    if hero_post:
        random_idx = random.randint(0, 2)
        insert_idx = min(random_idx, len(others))
        others.insert(insert_idx, hero_post)
        
    return others