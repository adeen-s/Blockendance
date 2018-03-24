import datetime as dt
import hashlib
from flask import Flask, request, render_template

from genesis import create_genesis_block
from newBlock import *
from block import *

app = Flask(__name__)

def checkIntegrity(chain):
    for i, block in enumerate(chain):
        if i < len(chain) - 1:
            print("Checking integrity of block {}".format(i))
            if block.hash_block() != chain[i+1].prev_hash:
                print("Chain has been modified at block index {}".format(i))
                break
        else:
            print("Chain has not been modified")

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

for i, block in enumerate(blockchain):
    if(i == 15):
        block.data = "Hello There, Data changed"
    print(block.data)

checkIntegrity(blockchain)

@app.route('/', methods=['GET'])
def hello():
    return render_template("index.html", name="Adeen", date=dt.date.today())

@app.route('/', methods=['POST'])
def parse_request():
    if(request.form.get("number")):
        return render_template("attendance.html", number=request.form.get("number"))
    elif(request.form.get("roll_no")):
        return
    return "Invalid POST request. This incident has been recorded."
