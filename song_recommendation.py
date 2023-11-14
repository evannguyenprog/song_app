import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '724086c08ef04c05a8b4b024d59ef0e3'
client_secret = '0bcf065450cd47289b378b98f8ba0533'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_info(track_title, artist):
    try:

        query = f"{track_title} artist:{artist}"
        results = sp.search(q=query, type='track', limit=1)
        track = results['tracks']['items'][0]
        audio_features = sp.audio_features([track['id']])[0]

        song_info = {
            'track_name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'release_date': track['album']['release_date'],
            'bpm': audio_features['tempo'],
            'key': audio_features['key'],
            'mode': audio_features['mode'],
        }

        return song_info
    except Exception as e:
        print(f"Error: {e}")
        return None
    

if __name__ == "__main__":
    
    track_name = input("Enter song: ")
    artist = input("Enter the artist: ")
    

    song_info = get_song_info(track_name, artist)

    if song_info:
        print("\nSong Information:")
        for key, value in song_info.items():
            print(f"{key}: {value}")
    else:
        print("Failed to retrieve song information.")