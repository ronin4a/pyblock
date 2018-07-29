from flask import current_app
from hashlib import sha256
import json
import time

__DEBUG_PRINT__="\n\nHI\n\n"

class Block(object):

  """Base initialization for Block class."""

  def __init__(self, index, transactions, timestamp, previous_hash):
    self.index = index
    self.transactions = transactions
    self.timestamp = timestamp
    self.previous_hash = previous_hash

  def __str__(self):
    _print_self = "Index: %s\nTransactions: %s\nPrevious hash: %s" \
        %(self.index, self.transactions, self.previous_hash)
    return(_print_self)

  """Computes the hash value of the block. This is essentially the SHA256 hash of
     the json.dumps output of the values in the block"""
  def compute_hash(self):
    """ A function that creates the hash of a block."""
    block_string = json.dumps(self.__dict__, sort_keys=True)
    return sha256(block_string.encode()).hexdigest()

class Blockchain(object):

  # difficulty of PoW algorithm
  difficulty = 2

  """Base initialization for Blockchain class."""

  def __init__(self):
    self.unconfirmed_transactions = [] # data yet to go into blockchain
    self.chain = []
    self.create_genesis_block()

  def __str__(self):
    """Outputs unconfirmed transactions."""
    print("Current unconfirmed transactions:")
    for tx in self.unconfirmed_transactions:
      print(tx)

  def create_genesis_block(self):
    """Generates genesis block and appends it to the chain. This block has an
       index of 0, previous_hash of 0 and a valid hash."""
    genesis_block = Block(0, [], time.time(), "0")
    genesis_block.hash = genesis_block.compute_hash()
    self.chain.append(genesis_block)

  @property
  def last_block(self):
    return self.chain[-1]

  """PoW processing for current blockchain."""

  def proof_of_work(self, block):
    """Function that tries different values of nonce to get a hash that
       satisfies our difficulty criteria."""
    block.nonce = 0

    computed_hash = block.compute_hash()
    while not computed_hash.startswith('0' * Blockchain.difficulty):
      block.nonce += 1
      computed_hash = block.compute_hash()

    return computed_hash

  """Adding blocks to the blockchain."""

  def add_block(self, block, proof):
    """A function for adding blocks to the chain after verification."""

    previous_hash = self.last_block.hash

    if previous_hash != block.previous_hash:
      return False

    if not self.is_valid_proof(block, proof):
      return False

    block.hash = proof
    self.chain.append(block)

    return True

  def is_valid_proof(self, block, block_hash):
    """Check if block_hash is valid hash of block and satisfies difficulty
       criteria. Checks that nonce + hash of block """
    return (block_hash.startswith('0' * Blockchain.difficulty) and \
            block_hash == block.compute_hash())

  """Mining mechanisms."""

  def add_new_transaction(self, transaction):
    self.unconfirmed_transactions.append(transaction)

  def mine(self):
    """Interface to add pending transactions to the blockchain by adding them
        to the block and figuring out Proof of Work."""

    print(self.unconfirmed_transactions)

    if not self.unconfirmed_transactions:
      return False

    last_block = self.last_block

    new_block = Block(index=last_block.index + 1,
                      transactions=self.unconfirmed_transactions,
                      timestamp=time.time(),
                      previous_hash=last_block.hash)
    proof = self.proof_of_work(new_block)
    self.add_block(new_block, proof)
    self.unconfirmed_transactions = []
    return new_block.index

  """Validations"""

  def check_chain_validity(cls, chain):
    """Check if block_hash is a valid hash, and confirm difficulty criteria."""

    result = True
    previous_hash = "0"

    for block in chain?:
      block_hash = block.hash
      # recompute hash
      delattr(block, "hash") #TODO check this - shouldn't this be compute_hash?

      if not (cls.is_valid_proof(block, block.hash)) or (previous_hash != block.previous_hash):
        result = False
      break

      block.hash, previous_hash = block_hash, block_hash

    return result
