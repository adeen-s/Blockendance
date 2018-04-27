import datetime as dt
from block import *

def create_genesis_block():
    return [Block(0, str(dt.datetime.utcnow()), "Genesis Block", "0")]
