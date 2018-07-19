from flask import Flask, request, abort
from flask import render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
import requests
import json
from block import app, blockchain

"""Standard web app functions."""
@app.route('/')
@app.route('/index')
@login_required
def index():
  """Landing page for blockchain app. Default should be front page with basic
     text information + login requirement. If user is logged in, then redirect
     toward transactions?"""
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
def get_pending_tx():
  return json.dumps(blockchain.unconfirmed_transactions)


@app.route('/pending_tx')
def get_pending_tx():
  return json.dumps(blockchain.unconfirmed_transactions)


