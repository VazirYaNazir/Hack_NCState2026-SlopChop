## SlopChop

AI-powered misinformation detection for social media. SlopChop analyzes posts using multi-modal AI detection to classify content as 'likely human,' 'uncertain,' or 'likely AI/scam.'

## Features

- **Multi-modal detection**: Analyzes both text and images
- **Real-time feed**: Live social media posts from X (Twitter)
- **Cross-platform**: Works on iOS and Android via Expo
- **Research-backed**: Informed by peer-reviewed misinformation research

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Expo Go app installed on your mobile device ([iOS](https://apps.apple.com/app/expo-go/id982107779) | [Android](https://play.google.com/store/apps/details?id=host.exp.exponent))

### 1. Get Your WiFi IP Address

**Windows:**
```bash
ipconfig
```
Look for "Wireless LAN adapter Wi-Fi" → IPv4 Address

**macOS:**
```bash
ipconfig getifaddr en0
```
Or go to System Preferences → Network → WiFi → Advanced → TCP/IP

**Linux:**
```bash
ip addr show | grep inet
```
Or:
```bash
hostname -I
```

### 2. Configure Environment Variables

**Frontend** (`frontend/.env`):
```env
EXPO_PUBLIC_API_URL=http://YOUR_IP_ADDRESS:5000
```

**Backend** (`backend/.env`) - *Required for live feed only*:
```env
API_KEY=""
API_KEY_SECRET=""
ACCESS_TOKEN=""
ACCESS_TOKEN_SECRET=""
BEARER_TOKEN=""
```

To use the live feed feature, you'll need X API credentials. Purchase credits at [X API Docs](https://docs.x.com/x-api)

### 3. Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 4. Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npx expo start
```

### 5. Connect Your Device

1. Open Expo Go on your mobile device
2. Scan the QR code displayed in your terminal
3. Wait for the app to load

**Ensure your mobile device and computer are on the same WiFi network**

## Research

SlopChop is informed by research showing that AI-generated misinformation:
- Receives **34% more likes** than traditional misinformation
- Gets **11% more retweets** despite originating from smaller accounts
- Often combines text and visual content (93% contain media)

## Troubleshooting

**App won't connect:**
- Verify both devices are on the same WiFi network
- Check that your IP address in `.env` is correct
- Ensure backend is running (check terminal for errors)
- Try restarting the Expo dev server

**Backend errors:**
- Verify all Python dependencies installed correctly
- Check that port 5000 is not in use by another application
- Ensure `.env` file exists in backend directory

**Live feed not working:**
- Verify X API credentials are correctly set in `backend/.env`
- Ensure you have active API credits
- Check API rate limits haven't been exceeded

## References

Chiara Drolsbach and Nicolas Pröllochs. 2025. Characterizing AI-Generated Misinformation on Social Media. arXiv:2505.10266 [cs.SI] (May 2025). https://doi.org/10.48550/arXiv.2505.10266