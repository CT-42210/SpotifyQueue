from flask import Flask, request, redirect, url_for, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import spotifySetup
import ngrok

load_dotenv()

client_id = os.getenv('ID')
client_secret = os.getenv('SECRET')
redirect_uri = os.getenv('REDIRECT')
username = os.getenv('USERNAME')
scope = 'user-modify-playback-state user-read-playback-state'

ngrok_authtoken = os.getenv('NGROK')

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

sp_oauth = SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                        username=username)

token_info = sp_oauth.get_cached_token()
if not token_info:
    spotifySetup.authenticate(scope, client_id, client_secret, redirect_uri, username)

sp = spotipy.Spotify(auth=token_info['access_token'])


@app.route('/', methods=['GET', 'POST'])
def index():
    playback_info = sp.current_playback()
    if playback_info is None:
        current_track = {'artists': [{'name': 'No Song Playing'}]}
    else:
        current_track = playback_info['item']

    if request.method == 'POST':
        song_name = request.form.get('song_name')
        if not song_name:
            return "Error: No search query provided", 400
        results = sp.search(q=song_name, limit=5, type='track')

        return render_template('results.html', results=results['tracks']['items'], current_track=current_track)

    return render_template('index.html', current_track=current_track)


@app.route('/play/<song_uri>')
def play(song_uri):
    sp.add_to_queue(song_uri)
    return redirect(url_for('index'))


if __name__ == '__main__':
    # port = ngrok.connect(authtoken=ngrok_authtoken, domain="spotifyqueue.ngrok.app", port="5000")
    # print(f"Ingress established at {port.url()}")
    app.run(debug=True)
