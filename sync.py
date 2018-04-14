import json
import os
from block import Block

def sync():
    blockchain = []
    blockchain_dir = "blockchain"
    if os.path.exists(blockchain_dir):
        for file in os.listdir(blockchain_dir):
            if file.endswith('.json'):
                filepath = "{}/{}".format(blockchain_dir, file)
                with open(filepath, 'r') as block_file:
                    json_block = json.load(block_file)
                    block = Block(**json_block)
                    blockchain.append(block)
    return blockchain
