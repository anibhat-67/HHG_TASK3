import os
import re
import serpapi
from dotenv import load_dotenv
import sys
import cv2

sys.stdout.reconfigure(encoding="utf-8")

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("SERPAPI_KEY")

if not API_KEY:
    print("ERROR: SERPAPI_KEY not found in .env")
    exit()

if len(sys.argv) > 1:
    image_path = sys.argv[1]
else:
    image_path = "input/reverse_search.jpg"

if not os.path.exists(image_path):
    print(f"ERROR: Image not found: {image_path}")
    exit()

# Resize/compress image to fit SerpApi's 500KB limit
os.makedirs("output", exist_ok=True)
temp_image_path = "output/temp_search.jpg"
img = cv2.imread(image_path)
if img is not None:
    height, width = img.shape[:2]
    max_dim = 600
    if max(height, width) > max_dim:
        scale = max_dim / max(height, width)
        img = cv2.resize(img, (int(width * scale), int(height * scale)))
    cv2.imwrite(temp_image_path, img, [cv2.IMWRITE_JPEG_QUALITY, 80])
    image_path = temp_image_path

# Create SerpApi client
client = serpapi.Client(api_key=API_KEY)

print("Uploading image to SerpApi...")
upload = client.upload_image(image_path)

if "error" in upload:
    print("Upload failed!")
    print(upload)
    exit()

image_id = upload.get("image_id")
if not image_id:
    print("Upload failed: No image_id returned.")
    print(upload)
    exit()

print(f"Image uploaded. ID: {image_id}")

# -----------------------------------
# STEP A: Google Lens — identify person
# -----------------------------------

print("\nSearching Google Lens...")

results = client.search({
    "engine": "google_lens",
    "image_id": image_id
})

if "error" in results:
    print("\nGoogle Lens search failed!")
    print(results["error"])
    exit()

# -----------------------------------
# Try to get identity from knowledge_graph
# -----------------------------------

knowledge_graph = results.get("knowledge_graph", {})
identified_name = (
    knowledge_graph.get("title") or
    knowledge_graph.get("name") or
    ""
).strip()

if identified_name:
    print(f"\nGoogle Lens identified person: {identified_name}")
    kg_link = knowledge_graph.get("link", "")

    # STEP B: targeted Google search for their real social media profile
    print(f"Running targeted search for: {identified_name}")
    search_results = client.search({
        "engine": "google",
        "q": f'"{identified_name}" site:twitter.com OR site:x.com OR site:linkedin.com OR site:instagram.com OR site:facebook.com',
        "num": 10
    })

    organic = search_results.get("organic_results", [])

    # Only match actual social media profile URLs
    social_patterns = [
        r"x\.com/[^/]+/?$",
        r"twitter\.com/[^/]+/?$",
        r"instagram\.com/[^/]+/?$",
        r"linkedin\.com/in/[^/]+/?$",
        r"facebook\.com/[^/]+/?$",
    ]

    discovered_url = ""
    for r in organic:
        link = r.get("link", "")
        if any(re.search(p, link) for p in social_patterns):
            discovered_url = link
            break

    # If no clean profile, take any social media link from results
    if not discovered_url:
        for r in organic:
            link = r.get("link", "")
            social_domains = ["x.com", "twitter.com", "instagram.com", "linkedin.com", "facebook.com"]
            if any(d in link for d in social_domains):
                discovered_url = link
                break

    # Last resort: knowledge graph link
    if not discovered_url:
        discovered_url = kg_link

    person_name = identified_name

else:
    # -----------------------------------
    # STEP B (fallback): parse visual_matches
    # -----------------------------------
    print("\nKnowledge graph not available. Analysing visual match titles...")

    visual_matches = results.get("visual_matches", [])

    print("\n================================")
    print("       GOOGLE LENS RESULTS")
    print("================================\n")

    if not visual_matches:
        print("No visual matches found.")
        exit()

    for i, match in enumerate(visual_matches, start=1):
        print(f"RESULT {i}")
        print(f"Title  : {match.get('title', 'N/A')}")
        print(f"Link   : {match.get('link', 'N/A')}")
        print(f"Source : {match.get('source', 'N/A')}")
        print("-" * 50)

    # --------------------------------------------------
    # Vote on the most likely person name from all titles
    # Strategy: extract capitalized 2-3 word Name Phrases
    # from titles, count frequency — the most common one
    # is likely the actual subject of the image.
    # --------------------------------------------------

    from collections import Counter

    name_pattern = re.compile(
        r"\b(?:Dr\.?\s+)?([A-Z][a-z]+ (?:[A-Z][a-z]+ )?[A-Z][a-z]+)\b"
    )

    JUNK_WORDS = {
        "Google Lens", "LinkedIn Profile", "Prime Minister",
        "Chief Executive", "Managing Director", "Executive Director",
        "Head Of", "Senior Director", "Research Foundation",
        "University Of", "Lunar And", "Planetary Institute"
    }

    name_counter = Counter()
    for match in visual_matches:
        title = match.get("title", "")
        for found in name_pattern.findall(title):
            if found not in JUNK_WORDS and len(found.split()) >= 2:
                name_counter[found] += 1

    voted_name = ""
    if name_counter:
        voted_name = name_counter.most_common(1)[0][0]
        print(f"\nMost likely person (by title vote): {voted_name}")

    if voted_name:
        # Do a targeted Google search using the voted name
        print(f"Running targeted search for: {voted_name}")
        search_results = client.search({
            "engine": "google",
            "q": f'"{voted_name}" site:twitter.com OR site:x.com OR site:linkedin.com OR site:instagram.com OR site:facebook.com',
            "num": 10
        })

        organic = search_results.get("organic_results", [])
        social_patterns = [
            r"x\.com/[^/]+/?$",
            r"twitter\.com/[^/]+/?$",
            r"instagram\.com/[^/]+/?$",
            r"linkedin\.com/in/[^/]+/?$",
            r"facebook\.com/[^/]+/?$",
        ]

        discovered_url = ""
        for r in organic:
            link = r.get("link", "")
            if any(re.search(p, link) for p in social_patterns):
                discovered_url = link
                break

        # If no clean profile, take any social media link
        if not discovered_url:
            for r in organic:
                link = r.get("link", "")
                social_domains = ["x.com", "twitter.com", "instagram.com", "linkedin.com", "facebook.com"]
                if any(d in link for d in social_domains):
                    discovered_url = link
                    break

        person_name = voted_name

    else:
        # Last resort: tiered visual match picking
        SKIP_DOMAINS = [
            "amazon", "ebay", "etsy", "getty", "shutterstock",
            "alamy", "pinterest", "wallpaper", "poster"
        ]

        def is_skippable(url):
            return any(s in url.lower() for s in SKIP_DOMAINS)

        def is_social_profile(url):
            profile_patterns = [
                r"x\.com/[^/]+/?$",
                r"twitter\.com/[^/]+/?$",
                r"instagram\.com/[^/]+/?$",
                r"facebook\.com/[^/]+/?$",
                r"linkedin\.com/in/[^/]+/?$",
                r"github\.com/[^/]+/?$",
            ]
            return any(re.search(p, url) for p in profile_patterns)

        def is_wikipedia(url):
            return "wikipedia.org/wiki/" in url

        def is_any_social(url):
            social = ["x.com", "twitter.com", "instagram.com",
                      "facebook.com", "linkedin.com", "youtube.com", "github.com"]
            return any(s in url for s in social)

        discovered_url = ""
        discovered_title = ""

        for match in visual_matches:
            link = match.get("link", "")
            if not is_skippable(link) and is_social_profile(link):
                discovered_url = link
                discovered_title = match.get("title", "")
                break

        if not discovered_url:
            for match in visual_matches:
                link = match.get("link", "")
                if not is_skippable(link) and is_wikipedia(link):
                    discovered_url = link
                    discovered_title = match.get("title", "")
                    break

        if not discovered_url:
            for match in visual_matches:
                link = match.get("link", "")
                if not is_skippable(link) and is_any_social(link):
                    discovered_url = link
                    discovered_title = match.get("title", "")
                    break

        if not discovered_url:
            for match in visual_matches:
                link = match.get("link", "")
                if not is_skippable(link):
                    discovered_url = link
                    discovered_title = match.get("title", "")
                    break

        if not discovered_url:
            discovered_url = visual_matches[0].get("link", "")
            discovered_title = visual_matches[0].get("title", "")

        # Clean up name from page title
        person_name = discovered_title
        for sep in [" - ", " | ", ": ", " – "]:
            if sep in discovered_title:
                person_name = discovered_title.split(sep)[0].strip()
                break

        person_name = re.sub(r"\s*\(@[^)]+\).*$", "", person_name).strip()
        person_name = re.sub(
            r"\s*[•|·]\s*(Facebook|Instagram|Twitter|LinkedIn|YouTube|X).*$",
            "", person_name, flags=re.IGNORECASE
        ).strip()

# -----------------------------------
# Save results
# -----------------------------------

os.makedirs("output", exist_ok=True)
with open("output/discovered_url.txt", "w") as f:
    f.write(discovered_url)
with open("output/discovered_name.txt", "w", encoding="utf-8") as f:
    f.write(person_name)

print(f"\nIdentified as : {person_name}")
print(f"URL saved     : {discovered_url}")