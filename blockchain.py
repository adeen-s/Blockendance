import datetime as dt
import hashlib
from flask import Flask, request, render_template

from genesis import create_genesis_block
from newBlock import *
from block import *

app = Flask(__name__)

blockchain = create_genesis_block()
previous_block = blockchain[0]

def add_block(form):
    data = []
    i = 1
    global previous_block
    while form.get("roll_no{}".format(i)):
        data.append(form.get("roll_no{}".format(i)))
        i += 1
    block_to_add = next_block(previous_block, data)
    blockchain.append(block_to_add)
    previous_block = block_to_add
    print ("Block #{} has been added to the blockchain!".format(block_to_add.index))
    print ("Hash: {}\n".format(block_to_add.hash))
    print(data)
    return "Block #{} has been added to the blockchain!".format(block_to_add.index)

@app.route('/',  methods = ['GET'])
def index():
    return render_template("index.html")

@app.route('/', methods = ['POST'])
def parse_request():
    if(request.form.get("name")):
        return render_template("class.html",
                                name = request.form.get("name"),
                                date = dt.date.today())
    elif(request.form.get("number")):
        return render_template("attendance.html",
                                course = request.form.get("course"),
                                year = request.form.get("year"),
                                number = int(request.form.get("number")))
    elif(request.form.get("roll_no1")):
        return add_block(request.form)

    else:
        return "Invalid POST request. This incident has been recorded."

if __name__ == "__main__":
    main()
