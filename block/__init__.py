from flask import Flask, request
import requests
from block.block import Block, Blockchain

app = Flask(__name__)
blockchain = Blockchain()

from block import routes

