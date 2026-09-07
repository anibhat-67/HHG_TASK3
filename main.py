import subprocess
import sys
import os
import json

sys.stdout.reconfigure(encoding="utf-8")

print("================================")
print("   HH GOA TASK 3")
print(" Face Identification + Blockchain")
print("================================")

# -------------------------------
# STEP 1: INPUT IMAGE
# -------------------------------

if len(sys.argv) > 1:
    image_path = sys.argv[1]
else:
    image_path = "input/test2.jpeg"

print(f"\nInput image: {image_path}")

# -------------------------------
# STEP 2: FACE DETECTION & ENCODING
# -------------------------------

print("\nRunning face detection and encoding...")

result = subprocess.run(
    [sys.executable, "face_process.py", image_path],
    capture_output=True,
    text=True,
    encoding="utf-8"
)

print(result.stdout)

if result.returncode != 0:
    print("Face processing failed!")
    print(result.stderr)
    sys.exit()

try:
    with open("output/face_data.json", "r") as f:
        face_data = json.load(f)
except FileNotFoundError:
    print("ERROR: face_data.json not found.")
    sys.exit()

total_faces = face_data.get("total_faces", 0)
if total_faces == 0:
    print("No faces to process.")
    sys.exit()

print(f"\nFound {total_faces} faces. Processing each individually...")

# -------------------------------
# STEP 3 & 4: REVERSE IMAGE SEARCH AND BLOCKCHAIN FOR EACH FACE
# -------------------------------

for face in face_data.get("faces", []):
    face_idx = face.get("face_index", 0) + 1
    crop_path = face.get("crop_path")
    confidence = face.get("det_score", 0) * 100
    conf_str = f"{confidence:.1f}%"

    print(f"\n{'='*40}")
    print(f"       PROCESSING FACE #{face_idx}")
    print(f"{'='*40}")

    if not crop_path or not os.path.exists(crop_path):
        print(f"Crop image not found for face #{face_idx}")
        continue

    url_file = "output/discovered_url.txt"
    name_file = "output/discovered_name.txt"
    if os.path.exists(url_file):
        os.remove(url_file)
    if os.path.exists(name_file):
        os.remove(name_file)

    print(f"\nRunning reverse image search for face #{face_idx}...")
    search_result = subprocess.run(
        [sys.executable, "reverse_search.py", crop_path],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    print(search_result.stdout)

    if search_result.returncode != 0:
        print(f"Reverse image search failed for face #{face_idx}!")
        print(search_result.stderr)
        continue

    try:
        with open(url_file, "r") as f:
            discovered_url = f.read().strip()
    except FileNotFoundError:
        discovered_url = ""

    if not discovered_url:
        print(f"No discovered URL found for face #{face_idx}!")
        continue

    try:
        with open(name_file, "r", encoding="utf-8") as f:
            discovered_name = f.read().strip()
    except FileNotFoundError:
        discovered_name = "Unknown"

    print("\n--------------------------------")
    print(f"       IDENTIFIED: FACE #{face_idx}")
    print("--------------------------------")
    print(f"Name       : {discovered_name}")
    print(f"URL        : {discovered_url}")
    print(f"Confidence : {conf_str}")

    print("\nStoring result on blockchain...")
    blockchain_result = subprocess.run(
        [sys.executable, "blockchain_verify.py",
         discovered_url,
         discovered_name,
         "1", # individual face
         conf_str],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    print(blockchain_result.stdout)
    if blockchain_result.returncode != 0:
        print(f"Blockchain verification failed for face #{face_idx}!")
        print(blockchain_result.stderr)

print("\n================================")
print("        TASK COMPLETED")
print("================================")