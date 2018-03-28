from block import *
import datetime as dt

def next_block(last_block, data):
    this_index = last_block.index + 1
    this_timestamp = dt.datetime.now()
    this_data = data
    this_prev_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_prev_hash)
