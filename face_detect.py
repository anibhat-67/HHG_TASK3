import cv2
import os

# -----------------------------------
# 1. SET INPUT AND OUTPUT PATHS
# -----------------------------------

input_path = "input/person.jpg.jpeg"
output_path = "output/detected_face.jpg"


# -----------------------------------
# 2. LOAD THE IMAGE
# -----------------------------------

image = cv2.imread(input_path)

if image is None:
    print("ERROR: Could not find the image!")
    print(f"Expected image at: {input_path}")
    exit()


# -----------------------------------
# 3. CONVERT IMAGE TO GRAYSCALE
# -----------------------------------

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# -----------------------------------
# 4. LOAD OPENCV FACE DETECTOR
# -----------------------------------

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


# -----------------------------------
# 5. DETECT FACES
# -----------------------------------

faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(50, 50)
)


# -----------------------------------
# 6. DISPLAY NUMBER OF FACES
# -----------------------------------

print(f"\nFaces detected: {len(faces)}")


# -----------------------------------
# 7. DRAW RECTANGLE AROUND FACE
# -----------------------------------

for (x, y, w, h) in faces:

    cv2.rectangle(
        image,
        (x, y),
        (x + w, y + h),
        (0, 255, 0),
        3
    )

    print(f"Face found at:")
    print(f"X: {x}, Y: {y}")
    print(f"Width: {w}, Height: {h}")


# -----------------------------------
# 8. CREATE OUTPUT FOLDER IF NEEDED
# -----------------------------------

os.makedirs("output", exist_ok=True)


# -----------------------------------
# 9. SAVE THE RESULT IMAGE
# -----------------------------------

cv2.imwrite(output_path, image)

print(f"\nResult saved to: {output_path}")


# -----------------------------------
# 10. FINAL RESULT
# -----------------------------------

if len(faces) > 0:
    print("\nFACE DETECTION SUCCESSFUL ✓")
else:
    print("\nNO FACE DETECTED ❌")