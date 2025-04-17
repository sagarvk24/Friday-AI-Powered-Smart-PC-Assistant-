import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

class SpotifyController:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
        ))

    def play_playlist(self, playlist_name):
        results = self.sp.current_user_playlists(limit=50)
        for item in results["items"]:
            if playlist_name.lower() in item["name"].lower():
                uri = item["uri"]
                self.sp.start_playback(context_uri=uri)
                return f"🎶 Playing playlist: {item['name']} on Spotify!"
        return "Sorry, I couldn't find that playlist in your Spotify."

    def play_song(self, song_name):
        results = self.sp.search(q=song_name, type='track', limit=1)
        tracks = results.get('tracks', {}).get('items', [])
        if not tracks:
            return "Sorry, I couldn't find that song."

        uri = tracks[0]['uri']
        name = tracks[0]['name']
        artist = tracks[0]['artists'][0]['name']

        try:
            self.sp.start_playback(uris=[uri])
            return f"🎵 Playing {name} by {artist}!"
        except spotipy.SpotifyException as e:
            if "NO_ACTIVE_DEVICE" in str(e):
                return "⚠️ Please open Spotify and play something once to activate your device."
            return f"❌ Spotify error: {e}"


if __name__ == "__main__":
    sc = SpotifyController()
    print(sc.play_song("Dance ka Bhoot"))
