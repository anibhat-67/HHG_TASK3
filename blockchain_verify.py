import hashlib
import json
import time
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

CHAIN_FILE = "output/blockchain.json"


# ─────────────────────────────────────────
# Block & Blockchain classes
# ─────────────────────────────────────────

class Block:
    def __init__(self, index, data, previous_hash, timestamp=None):
        self.index = index
        self.timestamp = timestamp if timestamp else time.time()
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
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }


class Blockchain:
    def __init__(self):
        self.chain = []
        self._load_or_create()

    def _load_or_create(self):
        """Load chain from disk if it exists, otherwise create genesis block."""
        if os.path.exists(CHAIN_FILE):
            with open(CHAIN_FILE, "r") as f:
                raw = json.load(f)
            for b in raw:
                block = Block(
                    b["index"], b["data"], b["previous_hash"],
                    timestamp=b["timestamp"]
                )
                # Restore saved hash (don't recalculate to preserve chain)
                block.hash = b["hash"]
                self.chain.append(block)
            print(f"Loaded existing blockchain ({len(self.chain)} blocks)")
        else:
            genesis = Block(0, {"message": "HH Goa Task 3 Genesis Block"}, "0")
            self.chain.append(genesis)
            print("Created new blockchain (genesis block)")

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), data, previous_block.hash)
        self.chain.append(new_block)
        self._save()
        return new_block

    def _save(self):
        os.makedirs("output", exist_ok=True)
        with open(CHAIN_FILE, "w") as f:
            json.dump([b.to_dict() for b in self.chain], f, indent=2)

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def print_chain(self):
        print("\n==============================")
        print("     FULL BLOCKCHAIN LEDGER")
        print("==============================")
        for block in self.chain:
            print(f"\n  Block #{block.index}")
            if block.index == 0:
                print(f"  [Genesis Block]")
            else:
                d = block.data
                print(f"  Person   : {d.get('person_name', 'Unknown')}")
                print(f"  URL      : {d.get('post_url', '')}")
                print(f"  Faces    : {d.get('faces_detected', '?')}")
                print(f"  Conf.    : {d.get('top_face_confidence', '?')}")
                ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp))
                print(f"  Time     : {ts}")
            print(f"  Hash     : {block.hash[:20]}...")
            print(f"  Prev     : {block.previous_hash[:20]}...")
            print("  " + "-" * 40)


# ─────────────────────────────────────────
# Main
# ─────────────────────────────────────────

if len(sys.argv) < 2:
    print("ERROR: Please provide a post URL.")
    print("Usage: python blockchain_verify.py <url> [person_name] [faces] [confidence]")
    sys.exit(1)

post_url    = sys.argv[1]
person_name = sys.argv[2] if len(sys.argv) > 2 else "Unknown"
faces_det   = sys.argv[3] if len(sys.argv) > 3 else "?"
confidence  = sys.argv[4] if len(sys.argv) > 4 else "?"

post_hash = hashlib.sha256(post_url.encode()).hexdigest()

data = {
    "post_url":           post_url,
    "post_hash":          post_hash,
    "person_name":        person_name,
    "faces_detected":     faces_det,
    "top_face_confidence": confidence
}

blockchain = Blockchain()
block = blockchain.add_block(data)

print("\n==============================")
print("      NEW BLOCKCHAIN RECORD")
print("==============================")
print(f"\n  Block index  : {block.index}")
print(f"  Person name  : {person_name}")
print(f"  Faces found  : {faces_det}")
print(f"  Confidence   : {confidence}")
print(f"  Post URL     : {post_url}")
print(f"  URL hash     : {post_hash[:32]}...")
print(f"  Block hash   : {block.hash[:32]}...")
print(f"\nBlockchain valid: {blockchain.verify_chain()}")
print(f"Total blocks   : {len(blockchain.chain)}")

blockchain.print_chain()