from flask import Flask, request
import requests
from app.block import Block, Blockchain

app = Flask(__name__)
blockchain = Blockchain()

from app import routes
