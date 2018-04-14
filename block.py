import hashlib
import os
import json
import datetime as dt
class Block:
    def __init__(self, index, timestamp, data, prev_hash, hash=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        if not hash:
            self.hash = self.hash_block()

    def hash_block(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode() + str(self.timestamp).encode() + str(self.data).encode() + str(self.prev_hash).encode())
        return sha.hexdigest()

    def toJSON(self):
        return json.dumps(self, default = lambda o: o.__dict__, sort_keys = True, indent = 4)

    def save_file(self):
        blockchain_dir = "blockchain"
        if not os.path.exists(blockchain_dir):
            os.mkdir(blockchain_dir)
        index_string = str(self.index).zfill(6)
        filename = "{}/{}.json".format(blockchain_dir, index_string)
        with open(filename, 'w') as block_file:
            block_file.write(self.toJSON())

# if __name__ == "__main__":
#     genesis = Block(0, str(dt.datetime.utcnow()), "Genesis Block", "0")
#     genesis.save_file()
