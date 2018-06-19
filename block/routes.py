from flask import Flask, request
import requests
import json
from block import app, blockchain

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

