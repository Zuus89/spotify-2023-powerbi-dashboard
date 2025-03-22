import pandas as pd

# Set input and output paths
input_path = "../data/spotify_2023_with_album_covers.csv"
output_path = "../data/spotify_2023_with_album_covers_utf8.csv"

# Step 1: Load the CSV using ISO-8859-1 encoding
df = pd.read_csv(input_path, encoding="ISO-8859-1")

# Step 2: Save the CSV again using UTF-8 encoding
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"✅ File exported with UTF-8 encoding at: {output_path}")
