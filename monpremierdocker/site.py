from flask import Flask,request
from datetime import datetime
import os
import socket

app = Flask(__name__)
hostname = socket.gethostname()
message = "" # A compléter, faites vous plaisir 

@app.route("/")
def main():
    print(request.remote_addr)
    return "<p>"+message+" <br> Server "+hostname+ " "+ str(datetime.now())+"</p>"