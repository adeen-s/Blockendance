import datetime as dt
from block import Block

def create_genesis_block():
    """
    Create the genesis block (first block in the blockchain)
    """
    genesis_data = {
        "type": "genesis",
        "message": "Genesis Block - Blockchain Initialized",
        "creator": "Blockendance System"
    }
    return Block(0, dt.datetime.now(), genesis_data, "0")

def create_blockchain():
    """
    Initialize a new blockchain with the genesis block
    """
    return [create_genesis_block()]
