from flask import Flask, request, redirect, url_for, session, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up your Spotify developer credentials
client_id = '01468e22e5fc423586658612d5f5f9ed'
client_secret = '571693f03b6d4c0099064d69ff920624'
redirect_uri = 'http://localhost:5000/callback'
username = 'tdbxvzlwqn9f4md0p81abbk3a'
scope = 'user-modify-playback-state user-read-playback-state'

app = Flask(__name__)
app.secret_key = 'ohyeabbg'

sp_oauth = SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                        username=username)


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'token_info' not in session:
        return redirect(url_for('login'))

    sp_oauth = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri=redirect_uri,
                            scope=scope)

    # Refresh the access token if it has expired
    if sp_oauth.is_token_expired(session['token_info']):
        session['token_info'] = sp_oauth.refresh_access_token(session['token_info']['refresh_token'])

    sp = spotipy.Spotify(auth=session['token_info']['access_token'])
    playback_info = sp.current_playback()
    current_track = playback_info['item']
    if current_track == None:
        current_track = 'No Song Playing'


    print(session['played_songs'])

    if request.method == 'POST':
        song_name = request.form.get('song_name')
        if not song_name:
            return "Error: No search query provided", 400
        results = sp.search(q=song_name, limit=20, type='track')

        return render_template('results.html', results=results['tracks']['items'], current_track=current_track)

    return render_template('index.html', current_track=current_track)

@app.route('/callback')
def callback():
    code = request.args.get('code')

    token_info = sp_oauth.get_access_token(code)

    session['token_info'] = token_info

    return redirect(url_for('index'))


@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/play/<song_uri>')
def play(song_uri):
    if 'token_info' not in session:
        return redirect(url_for('login'))

    sp = spotipy.Spotify(auth=session['token_info']['access_token'])

    sp.add_to_queue(song_uri)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
