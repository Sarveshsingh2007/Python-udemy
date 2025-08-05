from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# --- Spotify API credentials ---
CLIENT_ID = "32b1c57c9377465aa103d884cd48b363"
CLIENT_SECRET = "94c7ec5a55084022973a64ba104de2a2"

# --- Get date from user ---
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = date.split("-")[0]

# --- Scrape Billboard ---
header = {"User-Agent": "Mozilla/5.0"}
url = "https://www.billboard.com/charts/hot-100/" + date
response = requests.get(url, headers=header)
soup = BeautifulSoup(response.text, "html.parser")

# --- Extract songs ---
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
print(f"✅ Scraped {len(song_names)} songs from Billboard.")

# --- Authenticate with Spotify ---
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://billboardtospotify.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(f"🎵 Spotify User ID: {user_id}")

# --- Search for each song on Spotify ---
song_uris = []
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"❌ '{song}' doesn't exist in Spotify. Skipped.")
print(f"🎧 Total songs found on Spotify: {len(song_uris)}")

# --- Create a private playlist ---
playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{date} Billboard 100",
    public=False,
    description=f"Top 100 songs from Billboard on {date}"
)
print(f"📀 Playlist created: {playlist['external_urls']['spotify']}")

# --- Add songs to the playlist ---
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print("✅ Songs added to the playlist successfully.")
