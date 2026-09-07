import os
import serpapi
from dotenv import load_dotenv
import sys

sys.stdout.reconfigure(encoding="utf-8")

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("SERPAPI_KEY")

if not API_KEY:
    print("ERROR: SERPAPI_KEY not found in .env")
    exit()

# Image to search
image_path = "input/reverse_search.jpg"

if not os.path.exists(image_path):
    print(f"ERROR: Image not found: {image_path}")
    exit()

print("Uploading image to SerpApi...")

# Create SerpApi client
client = serpapi.Client(api_key=API_KEY)

# Upload local image
upload = client.upload_image(image_path)

# Check upload result
if "error" in upload:
    print("Upload failed!")
    print(upload)
    exit()

image_id = upload.get("image_id")

if not image_id:
    print("Upload failed: No image_id returned.")
    print(upload)
    exit()

print("Image uploaded successfully!")
print(f"Image ID: {image_id}")

# -----------------------------------
# Search using Google Lens
# -----------------------------------

print("\nSearching Google Lens...")

results = client.search({
    "engine": "google_lens",
    "image_id": image_id
})

# Check for errors
if "error" in results:
    print("\nGoogle Lens search failed!")
    print(results["error"])
    exit()

# -----------------------------------
# Display results
# -----------------------------------

print("\n================================")
print("       GOOGLE LENS RESULTS")
print("================================\n")

visual_matches = results.get("visual_matches", [])

if not visual_matches:
    print("No visual matches found.")
else:

    for i, match in enumerate(visual_matches, start=1):

        print(f"RESULT {i}")
        print(f"Title  : {match.get('title', 'N/A')}")
        print(f"Link   : {match.get('link', 'N/A')}")
        print(f"Source : {match.get('source', 'N/A')}")
        print("-" * 50)
        # Save the first result URL
if visual_matches:
    discovered_url = visual_matches[0].get("link", "")

    with open("output/discovered_url.txt", "w") as f:
        f.write(discovered_url)

    print(f"\nURL saved: {discovered_url}")