import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Replace these with your own values
client_id = 'your_client_id'
client_secret = 'your_client_secret'

# Set up the Spotify API client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_song(title, artist=None):
    try:
        # Construct the query based on whether the artist is provided
        if artist:
            query = f"track:{title} artist:{artist}"
        else:
            query = f"track:{title}"

        # Use the search endpoint to look for potential matches
        results = sp.search(q=query, type='track', market='US', limit=5)

        # Extract relevant information from the results
        potential_results = []
        for track in results['tracks']['items']:
            potential_results.append({
                'track_name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'release_date': track['album']['release_date'],
                'id': track['id'],
            })

        return potential_results

    except Exception as e:
        print(f"Error: {e}")
        return None

def get_song_info(track_id):
    try:
        # Get track details using the track ID
        track = sp.track(track_id)

        # Get audio features including BPM
        audio_features = sp.audio_features([track_id])[0]

        # Extract relevant information
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
    # Prompt the user for the song title and optional artist
    track_title = input("Enter the title of the song: ")
    artist = input("Enter the artist (press Enter to skip): ")

    # Search for potential matches
    potential_results = search_song(track_title, artist)

    if potential_results:
        print("\nPotential Matches:")
        for i, result in enumerate(potential_results, start=1):
            print(f"{i}. {result['track_name']} by {result['artist']}")

        choice = input("Enter the number of the desired match (or press Enter to exit): ")

        if choice.strip() and choice.isdigit() and 1 <= int(choice) <= len(potential_results):
            selected_track_id = potential_results[int(choice) - 1]['id']

            # Retrieve detailed information for the selected track
            song_info = get_song_info(selected_track_id)

            if song_info:
                print("\nSong Information:")
                for key, value in song_info.items():
                    print(f"{key}: {value}")
            else:
                print("\nFailed to retrieve detailed song information.")
    else:
        print("\nNo potential matches found.")
