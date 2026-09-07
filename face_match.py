import cv2
import numpy as np
import sys
import os
from insightface.app import FaceAnalysis

# -------------------------------
# FILE PATHS
# -------------------------------

registered_embeddings_folder = "registered_embeddings"

if len(sys.argv) > 1:
    test_image_path = sys.argv[1]
else:
    test_image_path = "input/test.jpeg"


# -------------------------------
# LOAD INSIGHTFACE MODEL
# -------------------------------

print("Loading face recognition model...")

app = FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"]
)

app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)


# -------------------------------
# LOAD TEST IMAGE
# -------------------------------

print(f"\nTesting image: {test_image_path}")

image = cv2.imread(test_image_path)

if image is None:
    print("ERROR: Could not find test image.")
    sys.exit(1)


# -------------------------------
# DETECT FACE
# -------------------------------

faces = app.get(image)

if len(faces) == 0:
    print("NO FACE DETECTED")
    sys.exit()

print(f"Faces detected in test image: {len(faces)}")


# -------------------------------
# GET TEST FACE EMBEDDING
# -------------------------------

test_embedding = faces[0].embedding


# -------------------------------
# COMPARE WITH ALL REGISTERED PEOPLE
# -------------------------------

best_person = None
best_similarity = -1

print("\n==============================")
print("       FACE COMPARISONS")
print("==============================")

for filename in os.listdir(registered_embeddings_folder):

    if not filename.endswith(".npy"):
        continue

    embedding_path = os.path.join(
        registered_embeddings_folder,
        filename
    )

    stored_embedding = np.load(embedding_path)

    # Calculate cosine similarity
    similarity = np.dot(stored_embedding, test_embedding) / (
        np.linalg.norm(stored_embedding) *
        np.linalg.norm(test_embedding)
    )

    person_name = os.path.splitext(filename)[0]

    print(f"{person_name}: {similarity * 100:.2f}%")

    # Keep the highest similarity
    if similarity > best_similarity:
        best_similarity = similarity
        best_person = person_name


# -------------------------------
# DISPLAY BEST RESULT
# -------------------------------

print("\n==============================")
print("       FACE MATCH RESULT")
print("==============================")

print(f"\nBest similarity: {best_similarity:.4f}")
print(f"Best similarity percentage: {best_similarity * 100:.2f}%")


# -------------------------------
# MATCH DECISION
# -------------------------------

threshold = 0.5

if best_similarity >= threshold:

    print("\nRESULT: MATCH")
    print(f"Person: {best_person}")

else:

    print("\nRESULT: NO MATCH")