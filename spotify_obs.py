import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import requests
from pathlib import Path

# Settings for Spotify API
CLIENT_ID = '1111'  # Replace with your Client ID
CLIENT_SECRET = '1111'  # Replace with your Client Secret
REDIRECT_URI = 'http://127.0.0.1:8080'  # Or the other Redirect URI you specified

# Authentication settings
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope='user-read-currently-playing'))

def get_current_track():
    try:
      # Get information about the current track
        current_track = sp.current_user_playing_track()
        if current_track is None:
            return "No active track", None

        track_name = current_track['item']['name']
        artist_name = current_track['item']['artists'][0]['name']
        # Get the URL of the cover
        image_url = current_track['item']['album']['images'][0]['url'] if current_track['item']['album']['images'] else None

        # Format the track name for scrolling
        full_text = f"{track_name} - {artist_name}"
        MAX_LENGTH = 50  # Maximum length of text before scrolling

        if len(full_text) > MAX_LENGTH:
            # Create a running line effect by adding spaces at the beginning and end of the line
            padding = " " * 10  # Add indents for smoothness
            scrolling_text = padding + full_text + padding
            formatted_text = scrolling_text
        else:
            formatted_text = full_text

        return formatted_text, image_url

    except Exception as e:
        return f"Erorr: {str(e)}", None

def download_image(image_url, filename='current_album_cover.jpg'):
    if image_url:
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            with open(filename, 'wb') as file:
                file.write(response.content)
            return True
        except Exception as e:
            print(f"Error downloading the image: {str(e)}")
            return False
    return False

def update_obs_file():
    while True:
        # Get the current track and the cover URL
        track_info, image_url = get_current_track()
        
        # Write the track name to a text file
        with open('current_song.txt', 'w', encoding='utf-8') as file:
            file.write(track_info)
        
        # Download and save the cover art if you have it
        if image_url:
            success = download_image(image_url)
            if success:
                print(f"The cover has been updated: {image_url}")
            else:
                print("Failed to update the cover.")
        else:
            print("No cover artwork found for the current track.")
        
        print(f"Updated: {track_info}")
        # Refresh every 5 seconds
        time.sleep(5)

if __name__ == "__main__":
    print("The program is up and running. Authorize to Spotify if required.")
    update_obs_file()
