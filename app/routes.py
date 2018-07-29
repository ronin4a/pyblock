"""CURRENTLY DOES NOT WORK"""

from flask import Flask, request, abort
from flask import render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
import requests
import json
import time
from app import app, blockchain

"""Standard web app functions."""
@app.route('/')
@app.route('/index')
@login_required
def index():
  """Landing page for blockchain app. Default should be front page with basic
     text information + login requirement. If user is logged in, then redirect
     toward transactions?"""
  print("HI")
  user = {'username': current_user}
  transactions = [
                  {}
                  ]
  return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['POST', 'GET'])
def login():
  """Standard login page for users."""
  return

@app.route('/logout')
def logout():
  """Standard logout page for users."""
  return

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
  """Standard edit profile page."""
  return

@app.route('/user/<username>')
def view_user():
  """View a user's public transactions. Still debating on whether we should make
     this public or private; default = private, maybe with a selection of
     public transactions? Or transactions between logged in user and <username>.
     """
  return


"""Blockchain-specific functions."""

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
  """Adds a new transaction to blockchain. Returns a message and then the error
     message (e.g. 404 error)."""
  tx_data = request.get_json()
  required_fields = ["author", "content"]

  for field in required_fields:
    if not tx_data.get(field):
      return "Invalid data transaction", 404

  tx_data["timestamp"] = time.time()

  blockchain.add_new_transaction(tx_data)

  return "Success", 201


@app.route('/chain', methods=['GET'])
def get_chain():
  chain_data = []
  for block in blockchain.chain:
    chain_data.append(block.__dict__)
  return json.dumps({"length": len(chain_data),
                     "chain": chain_data})


@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
  print("Mining...")
  result = blockchain.mine()
  if not result:
    return "No transactions to mine"
  return "Block ${} is mined.".format(result)


@app.route('/pending_tx')
def get_pending_tx():
  return json.dumps(blockchain.unconfirmed_transactions)

"""Network functions"""

# Add peers on the network
peers = set()

@app.route('/add_nodes', methods=['POST'])
def register_new_peers():
  nodes = request.get_json()
  if not nodes:
    return 'Invalid data', 400
  for node in nodes:
    peers.add(node)
  return 'Success', 201

def consensus():
  """Check for the consensus on the most valid chain; simple algorithm = simply pick the longest blockchain."""
  global blockchain

  longest_chain = None
  current_len = len(blockchain)

  for node in peers:
    response = requests.get('http://{}/chain'.format(node))
    length = response.json()['length']
    chain = response.json()['chain']
    if length > current_len and blockchain.check_chain_validity(chain):
      current_len = length
      longest_chain = chain

  if longest_chain:
    blockchain = longest_chain
    return True

  return False

@app.route('add_block', methods=['POST'])
def validate_and_add_block():
  """If a peer has a valid conensus block, add it to local blockchain."""
  block_data = request.get_json() #TODO What does request do exactly? It's imported from Flask...


