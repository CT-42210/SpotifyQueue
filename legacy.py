import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up your Spotify developer credentials
client_id = '01468e22e5fc423586658612d5f5f9ed'
client_secret = '571693f03b6d4c0099064d69ff920624'
redirect_uri = 'http://localhost:5000/'
username = 'tdbxvzlwqn9f4md0p81abbk3a'

scope = 'user-modify-playback-state user-read-playback-state'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, username=username))

# Search for a song
song_name = input("Enter a song name to search: ")
results = sp.search(q=song_name, limit=20, type='track')

# Print the search results and let the user select a song
print("Search results:")
for idx, track in enumerate(results['tracks']['items']):
    print(f"{idx+1}: {track['name']} - {track['artists'][0]['name']}")

song_selection = int(input("Enter the number of the song you want to add to the queue: ")) - 1
selected_song_uri = results['tracks']['items'][song_selection]['uri']

# Add the selected song to the queue
sp.add_to_queue(selected_song_uri)
print("Song added to the queue.")
