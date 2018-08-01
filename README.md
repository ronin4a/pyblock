# Description

First attempt at creating a basic blockchain in Python.

Currently based off an IBM tutorial, with some tweaks and restructuring for
better use of Python Flask.

## Latest update

Completed up to step 7 (not inclusive). Need to test:
- create transactions = works; but not saving

Test:
- /mine, /pending_tx, /chain

Dev
- web app content
- sqlalchemy db to store transactions/blocks/blockchain? does this defeat the
  purpose??


## Instructions

1. export FLASK_APP=pylock.py; export FLASK_DEBUG=1;
2. flask run
3. execute a few RESTful commands on routes in routes.py

## Future
- implement as a clearing house for bets made on Casino World

## Ref
- https://www.ibm.com/developerworks/cloud/library/cl-develop-blockchain-app-in-python/index.html
- https://github.com/satwikkansal/ibm_blockchain/blob/master/node_server.py
