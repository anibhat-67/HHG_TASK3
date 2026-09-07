import hashlib
import json
import time


class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True)

        return hashlib.sha256(
            block_string.encode()
        ).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []

        # Genesis block
        genesis = Block(
            0,
            {"message": "HH Goa Task 3 Genesis Block"},
            "0"
        )

        self.chain.append(genesis)

    def add_block(self, data):
        previous_block = self.chain[-1]

        new_block = Block(
            len(self.chain),
            data,
            previous_block.hash
        )

        self.chain.append(new_block)

        return new_block

    def verify_chain(self):
        for i in range(1, len(self.chain)):

            current = self.chain[i]
            previous = self.chain[i - 1]

            # Check current block's hash
            if current.hash != current.calculate_hash():
                return False

            # Check connection to previous block
            if current.previous_hash != previous.hash:
                return False

        return True
blockchain = Blockchain()

# -----------------------------------------
# STORE REAL SEARCH RESULT
# -----------------------------------------

import sys

if len(sys.argv) < 2:
    print("ERROR: Please provide a post URL.")
    print("Example:")
    print("python blockchain_verify.py https://example.com/post")
    exit()

post_url = sys.argv[1]

# Create fingerprint of the discovered URL
post_hash = hashlib.sha256(
    post_url.encode()
).hexdigest()

data = {
    "post_url": post_url,
    "post_hash": post_hash
}

block = blockchain.add_block(data)

print("\n==============================")
print("      BLOCKCHAIN RECORD")
print("==============================")

print(f"\nBlock index : {block.index}")
print(f"Post URL    : {post_url}")
print(f"Post hash   : {post_hash}")
print(f"Block hash  : {block.hash}")

print("\nBlockchain valid:", blockchain.verify_chain())