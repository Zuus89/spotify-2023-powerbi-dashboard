import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# ---------------------
# CONFIGURATION
# ---------------------
CLIENT_ID = "f8ee0e47dce544c9a4df44b44c98e75a"
CLIENT_SECRET = "34881330d81e4c6b900ce76872a87b0e"
CSV_PATH = "../data/spotify-2023.csv"
OUTPUT_PATH = "../data/spotify_2023_with_album_covers.csv"

# ---------------------
# AUTHENTICATION
# ---------------------
auth_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)
sp = spotipy.Spotify(auth_manager=auth_manager)

# ---------------------
# LOAD DATA
# ---------------------
df = pd.read_csv(CSV_PATH, encoding="ISO-8859-1")

# Optional: reduce for testing
# df = df.head(10)

df["album_cover_url"] = None  # New column

# ---------------------
# FETCH ALBUM COVERS
# ---------------------
for idx, row in df.iterrows():
    track = row["track_name"]
    artist = row["artist(s)_name"]
    query = f"track:{track} artist:{artist}"

    try:
        result = sp.search(q=query, type="track", limit=1)
        items = result.get("tracks", {}).get("items", [])

        if items:
            album_images = items[0]["album"]["images"]
            if album_images:
                df.at[idx, "album_cover_url"] = album_images[0]["url"]
        else:
            df.at[idx, "album_cover_url"] = "Not Found"

    except Exception as e:
        print(f"❌ Error fetching: {track} - {artist} → {e}")
        df.at[idx, "album_cover_url"] = "Error"

    # Respect API rate limits
    time.sleep(0.3)

# ---------------------
# SAVE TO CSV
# ---------------------
df.to_csv(OUTPUT_PATH, index=False)
print(f"✅ Finished! Album covers saved to: {OUTPUT_PATH}")