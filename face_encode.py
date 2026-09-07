import cv2
import numpy as np
from insightface.app import FaceAnalysis
import os

# -----------------------------
# FOLDERS
# -----------------------------

registered_folder = "registered"
embedding_folder = "registered_embeddings"

os.makedirs(embedding_folder, exist_ok=True)


# -----------------------------
# LOAD FACE MODEL
# -----------------------------

print("Loading face recognition model...")

app = FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"]
)

app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)


# -----------------------------
# PROCESS EACH PERSON
# -----------------------------

for filename in os.listdir(registered_folder):

    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    image_path = os.path.join(registered_folder, filename)

    print(f"\nProcessing: {filename}")

    image = cv2.imread(image_path)

    if image is None:
        print("Could not read image.")
        continue

    faces = app.get(image)

    if len(faces) == 0:
        print("No face detected.")
        continue

    # Take the first detected face
    face = faces[0]

    embedding = face.embedding

    # Person name = filename without extension
    person_name = os.path.splitext(filename)[0]

    output_path = os.path.join(
        embedding_folder,
        person_name + ".npy"
    )

    np.save(output_path, embedding)

    print(f"Embedding saved: {output_path}")


print("\nAll registered faces processed.")