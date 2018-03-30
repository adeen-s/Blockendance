import datetime as dt
import hashlib
from flask import Flask, request, render_template, Response

from genesis import create_genesis_block
from newBlock import next_block
from block import *

app = Flask(__name__)
response = Response()
response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')

blockchain = create_genesis_block()
previous_block = blockchain[0]
data = []

def add_block(form):
    global data
    data.append([])
    i = 1
    global previous_block
    while form.get("roll_no{}".format(i)):
        data[len(data) - 1].append(form.get("roll_no{}".format(i)))
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
    global data
    if(request.form.get("name")):
        data = []
        data.append(request.form.get("name"))
        data.append(str(dt.date.today()))
        return render_template("class.html",
                                name = request.form.get("name"),
                                date = dt.date.today())

    elif(request.form.get("number")):
        data = data[0:2]
        data.append(request.form.get("course"))
        data.append(request.form.get("year"))
        return render_template("attendance.html",
                                course = request.form.get("course"),
                                year = request.form.get("year"),
                                number = int(request.form.get("number")))
    elif(request.form.get("roll_no1")):
        data = data[0:4]
        return render_template("submitted.html", result = add_block(request.form))

    else:
        return "Invalid POST request. This incident has been recorded."

if __name__ == "__main__":
    main()
