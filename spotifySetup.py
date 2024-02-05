import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

client_id = os.getenv('ID')
client_secret = os.getenv('SECRET')
redirect_uri = os.getenv('REDIRECT')
username = os.getenv('USERNAME')
scope = 'user-modify-playback-state user-read-playback-state'

sp_oauth = SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                        username=username)

token_info = sp_oauth.get_cached_token()
if not token_info:
    auth_url = sp_oauth.get_authorize_url()
    print(f"Please navigate here: {auth_url}")
    response = input("Enter the URL you were redirected to: ")
    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)

# At this point, the token is cached, and you can run your main application
print("Token cached, you can now run the main application.")
