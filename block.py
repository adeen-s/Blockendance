import hashlib
import json

class Block:
    def __init__(self, index, timestamp, data, prev_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.hash_block()

    def hash_block(self):
        """
        Create a SHA-256 hash of the block contents
        """
        sha = hashlib.sha256()
        # Convert data to JSON string for consistent hashing
        data_string = json.dumps(self.data, sort_keys=True) if self.data else ""
        block_string = f"{self.index}{self.timestamp}{data_string}{self.prev_hash}"
        sha.update(block_string.encode('utf-8'))
        return sha.hexdigest()

    def __str__(self):
        """
        String representation of the block
        """
        return f"Block #{self.index} [Hash: {self.hash[:10]}...]"

    def __repr__(self):
        """
        Detailed representation of the block
        """
        return f"Block(index={self.index}, timestamp={self.timestamp}, hash={self.hash[:10]}...)"

    def to_dict(self):
        """
        Convert block to dictionary for JSON serialization
        """
        return {
            'index': self.index,
            'timestamp': str(self.timestamp),
            'data': self.data,
            'prev_hash': self.prev_hash,
            'hash': self.hash
        }

    def is_valid(self):
        """
        Validate the block's hash
        """
        return self.hash == self.hash_block()
