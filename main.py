import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

print("================================")
print("   HH GOA TASK 3")
print(" Face Identification + Blockchain")
print("================================")

# -------------------------------
# INPUT IMAGE
# -------------------------------

if len(sys.argv) > 1:
    image_path = sys.argv[1]
else:
    image_path = "input/test2.jpeg"

print(f"\nInput image: {image_path}")


# -------------------------------
# FACE MATCHING
# -------------------------------

print("\nRunning face matching...")

result = subprocess.run(
    [sys.executable, "face_match.py", image_path],
    capture_output=True,
    text=True
)

print(result.stdout)
if "RESULT: NO MATCH" in result.stdout:
    print("\nNo matching person found.")
    print("Stopping pipeline.")
    sys.exit()

if result.returncode != 0:
    print("Face matching failed!")
    print(result.stderr)
    sys.exit()


# -------------------------------
# REVERSE IMAGE SEARCH
# -------------------------------

print("\nRunning reverse image search...")

search_result = subprocess.run(
    [sys.executable, "reverse_search.py"],
    capture_output=True,
    text=True
)

print(search_result.stdout)

if search_result.returncode != 0:
    print("Reverse image search failed!")
    print(search_result.stderr)
    sys.exit()


# -------------------------------
# READ DISCOVERED URL
# -------------------------------

try:
    with open("output/discovered_url.txt", "r") as f:
        discovered_url = f.read().strip()

except FileNotFoundError:
    print("No discovered URL found!")
    sys.exit()


if not discovered_url:
    print("Discovered URL is empty!")
    sys.exit()


print("\nDiscovered URL:")
print(discovered_url)


# -------------------------------
# BLOCKCHAIN VERIFICATION
# -------------------------------

print("\nStoring result on blockchain...")

blockchain_result = subprocess.run(
    [sys.executable, "blockchain_verify.py", discovered_url],
    capture_output=True,
    text=True
)

print(blockchain_result.stdout)

if blockchain_result.returncode != 0:
    print("Blockchain verification failed!")
    print(blockchain_result.stderr)
    sys.exit()


# -------------------------------
# COMPLETE
# -------------------------------

print("\n================================")
print("        TASK COMPLETED")
print("================================")