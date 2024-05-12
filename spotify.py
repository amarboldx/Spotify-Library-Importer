import spotipy
import spotipy.util as util
import json
import os

class Spotify:
    scope = 'playlist-read-private user-read-playback-state user-library-read'

    def __init__(self, path):
        self.path = path

    def read_config(self):
        with open(self.path, 'r') as f:
            config = json.load(f)
        return config

    def spotify_auth_service(self):
        config = self.read_config()
        username = config["SPOTIFY_USER_ID"]
        client_id = config["SPOTIPY_CLIENT_ID"]
        client_secret = config["SPOTIPY_CLIENT_SECRET"]
        redirect_uri = config["SPOTIPY_REDIRECT_URI"]
        try: 
            token = util.prompt_for_user_token(username, self.scope, client_id, client_secret, redirect_uri)
        except:
            os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, self.scope)
        return spotipy.Spotify(auth=token)