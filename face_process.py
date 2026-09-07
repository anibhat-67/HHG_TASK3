import cv2
import sys
import json
import os
from insightface.app import FaceAnalysis

sys.stdout.reconfigure(encoding="utf-8")

if len(sys.argv) > 1:
    test_image_path = sys.argv[1]
else:
    test_image_path = "input/test.jpeg"

print("Loading face recognition model...")
app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0, det_size=(640, 640))

print(f"\nProcessing image: {test_image_path}")
image = cv2.imread(test_image_path)
if image is None:
    print("ERROR: Could not find image.")
    sys.exit(1)

faces = app.get(image)
if len(faces) == 0:
    print("NO FACE DETECTED")
    sys.exit(1)

print(f"\nFaces detected: {len(faces)}")
print("=" * 40)

face_data = []
for i, face in enumerate(faces):
    embedding = face.embedding
    det_score = float(face.det_score)
    bbox = face.bbox.tolist()

    # Gender and age from insightface
    gender = "Male" if face.gender == 1 else "Female"
    age = int(face.age)

    print(f"\nFace #{i+1}:")
    print(f"  Detection confidence : {det_score * 100:.1f}%")
    print(f"  Estimated gender     : {gender}")
    print(f"  Estimated age        : ~{age} years")
    print(f"  Embedding dimension  : {embedding.shape[0]}")

    # Crop the face from the image
    x1, y1, x2, y2 = [int(v) for v in bbox]
    # Add a little padding if possible
    h, w = image.shape[:2]
    padding = int(max(x2-x1, y2-y1) * 0.2)
    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(w, x2 + padding)
    y2 = min(h, y2 + padding)

    face_crop = image[y1:y2, x1:x2]
    os.makedirs("output/crops", exist_ok=True)
    crop_path = f"output/crops/face_{i}.jpg"
    cv2.imwrite(crop_path, face_crop)

    face_data.append({
        "face_index": i,
        "det_score": det_score,
        "gender": gender,
        "age": age,
        "bbox": bbox,
        "crop_path": crop_path
    })

# Save face data for main.py to consume
os.makedirs("output", exist_ok=True)
with open("output/face_data.json", "w") as f:
    json.dump({
        "total_faces": len(faces),
        "faces": face_data
    }, f, indent=2)

print(f"\n{'=' * 40}")
print(f"FACE DETECTION AND ENCODING COMPLETE")
print(f"Total faces processed: {len(faces)}")
