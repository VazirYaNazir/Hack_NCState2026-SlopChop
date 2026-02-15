import instaloader
import getpass

# 1. SETUP
L = instaloader.Instaloader()
USERNAME = "quackpromax"

print(f"🔐 Logging in as {USERNAME} to generate fresh session...")

# 2. LOGIN (Interactive)
try:
    # This will ask for your password safely in the terminal
    password = getpass.getpass(f"Enter password for {USERNAME}: ")
    
    L.login(USERNAME, password)
    print("Login Successful!")
    
    # 3. SAVE THE FILE
    filename = f"backend/session-{USERNAME}"
    L.save_session_to_file(filename=filename)
    print(f"Session saved to: {filename}")
    print("Now run your feed script again.")

except instaloader.TwoFactorAuthRequiredException:
    # Handle 2FA if you have it turned on
    code = input("Enter 2FA Code from SMS/App: ")
    L.two_factor_login(code)
    L.save_session_to_file(filename=f"backend/session-{USERNAME}")
    print("2FA Login Successful & Saved!")

except Exception as e:
    print(f"Login Failed: {e}")