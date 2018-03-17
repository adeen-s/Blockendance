import datetime as dt
import hashlib

class Block:
    def __init__(self, index, timestamp, data, prev_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode() + str(self.timestamp).encode() + str(self.data).encode() + str(self.prev_hash).encode())
        return sha.hexdigest()

def create_genesis_block():
    return [Block(0, dt.datetime.now(), "Genesis Block", "0")]

def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = dt.datetime.now()
    this_data = "Hey Adeen! I'm block " + str(this_index)
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)

blockchain = create_genesis_block()
previous_block = blockchain[0]

# blocks after the genesis block
num_of_blocks = 20

# Add blocks to the chain
for i in range(0, num_of_blocks):
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    previous_block = block_to_add
    print ("Block #{} has been added to the blockchain!".format(block_to_add.index))
    print ("Hash: {}\n".format(block_to_add.hash))

    for block in blockchain:
        print(block.data)
