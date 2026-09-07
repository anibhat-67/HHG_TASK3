# Face Recognition, Reverse Image Search & Blockchain Verification

## Overview

This project is an image verification system that combines **Face Detection, Face Recognition, Reverse Image Search, and Blockchain-based verification** into one pipeline.

The system takes a test image and performs the following operations:

1. Detects a face in the image.
2. Generates a face embedding for the detected face.
3. Compares the face with registered people.
4. Identifies the person with the highest similarity.
5. Performs a reverse image search using SerpApi.
6. Stores the discovered URL and its hash in a blockchain.
7. Verifies the integrity of the blockchain record.

The complete process can be executed using:

```bash
python main.py
```

---

# Project Workflow

```text
                 Test Image
                     |
                     v
              Face Detection
                     |
                     v
              Face Embedding
                     |
                     v
          Compare with Registered
                 Embeddings
                     |
                     v
              Face Match Result
                     |
                     v
          Reverse Image Search
                 (SerpApi)
                     |
                     v
             Discovered URL
                     |
                     v
              SHA-256 Hash
                     |
                     v
             Blockchain Record
                     |
                     v
             Blockchain Valid
```

---

# Technologies Used

- Python
- OpenCV
- NumPy
- InsightFace
- SerpApi
- SHA-256 Cryptographic Hashing
- Custom Python Blockchain

---

# Project Structure

```text
HHG_TASK3/
│
├── input/
│   ├── test.jpeg
│   ├── test2.jpeg
│   ├── test3.jpg
│   └── ...
│
├── output/
│   ├── detected_face.jpg
│   ├── discovered_url.txt
│   └── face_embedding.npy
│
├── registered/
│   ├── advaith.jpeg
│   ├── aniruddha.jpeg
│   ├── ashwatth.jpeg
│   └── ...
│
├── registered_embeddings/
│   ├── advaith.npy
│   ├── aniruddha.npy
│   ├── ashwatth.npy
│   └── ...
│
├── blockchain_verify.py
├── face_detect.py
├── face_encode.py
├── face_match.py
├── main.py
├── reverse_search.py
├── .env
└── .gitignore
```

---

# 1. Face Detection

### File: `face_detect.py`

The input image is processed using **InsightFace** to detect faces.

The program:

1. Loads the input image.
2. Detects faces in the image.
3. Determines the bounding box of the detected face.
4. Reports the face coordinates.
5. Saves the detected-face result in the output folder.

Example output:

```text
Faces detected: 1

Face found at:
X: 1118, Y: 1682
Width: 629, Height: 629

FACE DETECTION SUCCESSFUL
```

The detected face is saved as:

```text
output/detected_face.jpg
```

---

# 2. Face Encoding

### File: `face_encode.py`

Face encoding converts a detected face into a numerical representation called a **face embedding**.

InsightFace generates an embedding that represents important facial features.

The registered images are stored inside:

```text
registered/
```

For every registered person, the program generates an embedding and saves it as a NumPy file:

```text
registered_embeddings/
```

For example:

```text
registered/
├── advaith.jpeg
├── aniruddha.jpeg
└── ashwatth.jpeg
```

produces:

```text
registered_embeddings/
├── advaith.npy
├── aniruddha.npy
└── ashwatth.npy
```

To generate/update the registered embeddings:

```bash
python face_encode.py
```

If a new registered image is added to the `registered` folder, running the encoding program generates the corresponding embedding.

---

# 3. Face Matching

### File: `face_match.py`

The test image is converted into a face embedding and compared with all the embeddings stored in:

```text
registered_embeddings/
```

The system calculates **cosine similarity** between the test face and every registered face.

The highest similarity score is selected as the best match.

Example:

```text
==============================
       FACE COMPARISONS
==============================

advaith: 32.15%
aniruddha: 90.03%
ashwatth: 41.27%

==============================
       FACE MATCH RESULT
==============================

Best similarity: 0.9003
Best similarity percentage: 90.03%

RESULT: MATCH
Person: aniruddha
```

The matching threshold used in the program is:

```text
0.5
```

Therefore:

```text
similarity >= 0.5
```

results in:

```text
MATCH
```

while a lower similarity results in:

```text
NO MATCH
```

---

# 4. Reverse Image Search

### File: `reverse_search.py`

After the face matching stage, the test image is uploaded for reverse image searching using **SerpApi**.

SerpApi provides an API that allows the program to perform image search operations and retrieve search results.

The API key is stored in the environment file:

```text
.env
```

The program:

1. Loads the API key.
2. Creates a SerpApi client.
3. Uploads the image.
4. Performs the reverse image search.
5. Retrieves relevant search results.
6. Extracts a discovered URL.
7. Saves the discovered URL.

Example:

```text
Running reverse image search...

Discovered URL:
https://www.facebook.com/...
```

The discovered URL is also stored in:

```text
output/discovered_url.txt
```

---

# 5. Blockchain Verification

### File: `blockchain_verify.py`

The project uses a custom Python implementation of a blockchain.

This is a **local blockchain implementation created for the project**, rather than a public blockchain network such as Ethereum or Bitcoin.

Each block contains:

- Block index
- Timestamp
- Data
- Previous block hash
- Current block hash

The hash is generated using:

```text
SHA-256
```

The discovered URL is stored as blockchain data.

Before storing it, a SHA-256 hash of the URL is generated.

Example:

```text
Post URL:
https://www.facebook.com/...

Post hash:
426428c9cc0ec2a736e82b49528b289a0cd2dd48ef2b24682d3de9c0a001a3be

Block hash:
...
```

The blockchain then checks:

1. Whether the current block's hash is valid.
2. Whether the current block correctly points to the previous block.

Example:

```text
Blockchain valid: True
```

---

# 6. Complete Pipeline

### File: `main.py`

The `main.py` file combines all the individual stages into one automated workflow.

The complete pipeline is:

```text
Input Image
     |
     v
Face Detection
     |
     v
Face Embedding
     |
     v
Face Matching
     |
     v
Best Matching Person
     |
     v
Reverse Image Search
     |
     v
Discovered URL
     |
     v
URL SHA-256 Hash
     |
     v
Blockchain Storage
     |
     v
Blockchain Verification
```

Running:

```bash
python main.py
```

executes the complete process.

A different test image can be provided as an argument:

```bash
python main.py input/test3.jpg
```

---

# Example Complete Output

```text
FACE MATCH RESULT
==============================

Best similarity: 0.9003
Best similarity percentage: 90.03%

RESULT: MATCH
Person: aniruddha

Running reverse image search...

Discovered URL:
https://www.facebook.com/...

Storing result on blockchain...

Blockchain valid: True

==============================
       TASK COMPLETED
==============================
```

---

# Adding a New Registered Person

To register a new person:

### Step 1

Place the person's image inside:

```text
registered/
```

For example:

```text
registered/
└── aditya.jpeg
```

### Step 2

Run:

```bash
python face_encode.py
```

This creates:

```text
registered_embeddings/aditya.npy
```

### Step 3

The next time a test image is processed, the new embedding will also be included in the face comparison.

---

# Testing a New Image

Place the test image inside:

```text
input/
```

For example:

```text
input/test3.jpg
```

Run:

```bash
python main.py input/test3.jpg
```

The program will:

- Detect the face
- Compare it with registered embeddings
- Display the similarity percentages
- Determine the best match
- Perform reverse image search
- Store the discovered URL on the blockchain
- Verify the blockchain

---

# API Configuration

The reverse image search requires a **SerpApi API key**.

The key is stored in:

```text
.env
```

Example:

```text
SERPAPI_KEY=your_api_key_here
```

The API key should not be publicly shared.

The `.env` file is excluded from Git using `.gitignore`.

---

# Security and Data Handling

The project uses SHA-256 hashing for the blockchain records.

The purpose of hashing the discovered URL is to create a fixed cryptographic representation of the URL that can be stored in the blockchain record.

The blockchain also stores the hash of the previous block, creating a chain between blocks.

If a block's data is modified, its calculated hash will no longer match the stored hash, causing blockchain verification to fail.

---

# Limitations

- Face recognition accuracy depends on image quality, lighting, pose, and the detected face.
- The similarity threshold is fixed in the current implementation.
- Reverse image search depends on the availability and quality of search results.
- The blockchain is a custom local implementation for demonstration and verification purposes.
- The system currently processes the first detected face when multiple faces are present.
- The reverse image search requires an active SerpApi API key.

---

# How to Run

## 1. Activate the virtual environment

On Windows:

```bash
.venv\Scripts\activate
```

## 2. Run face encoding

```bash
python face_encode.py
```

## 3. Run the complete system

```bash
python main.py input/test3.jpg
```

---

# Individual Modules

Each module can also be tested separately.

### Face Detection

```bash
python face_detect.py
```

### Face Encoding

```bash
python face_encode.py
```

### Face Matching

```bash
python face_match.py input/test3.jpg
```

### Reverse Image Search

```bash
python reverse_search.py
```

### Blockchain Verification

```bash
python blockchain_verify.py "PASTE_DISCOVERED_URL_HERE"
```

### Complete Pipeline

```bash
python main.py input/test3.jpg
```

---

# Conclusion

This project demonstrates how multiple technologies can be combined into a single image verification pipeline.

The system combines:

```text
Computer Vision
      +
Face Recognition
      +
Reverse Image Search
      +
Cryptographic Hashing
      +
Blockchain Verification
```

The final system provides a way to identify a matching registered face, find possible online sources of the image, and record the discovered URL in a tamper-evident blockchain structure.

---

## Team
Aniruddha Bhat
Advaith S Shetty
Ashwath Patel
Developed as part of the HH Goa Task 3 project.