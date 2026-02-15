import pickle
import os


# Replace this with your exact filename
SESSION_FILENAME = "backend/session-quackpromax" 

def inspect():
    print(f"📂 Reading File: {SESSION_FILENAME}")
    print("-" * 40)

    if not os.path.exists(SESSION_FILENAME):
        print(f"Error: File '{SESSION_FILENAME}' not found.")
        return

    try:
        with open(SESSION_FILENAME, 'rb') as f:
            data = pickle.load(f)

        # CHECK TYPE
        if isinstance(data, dict):
            print("Type: Python Dictionary (Raw Cookies)")
            print(f"Keys Found: {list(data.keys())}")
            
            # Print specific valuable keys
            if 'sessionid' in data:
                # Mask it for security
                sid = data['sessionid']
                masked = sid[:6] + "******" + sid[-4:]
                print(f"🍪 Session ID: {masked} (Valid)")
            else:
                print("Error: 'sessionid' is MISSING. This file won't work.")
                
            if 'csrftoken' in data:
                print(f"🛡️ CSRF Token: Present")
            else:
                print("Warning: CSRF Token missing.")

        else:
            print(f"Unknown Type: {type(data)}")
            print("This script expects a dictionary format.")

    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    inspect()