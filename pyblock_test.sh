#!/bin/bash


if [[ $1 == "POST" ]]
then
  curl -POST 'http://localhost:5000/new_transaction' -H 'Content-TYpe: application/json' -d '
  {
    "author": "albert",
    "content": "my first post"
  }'
fi


if [[ $1 == "CHECK" ]]
then
  curl -GET 'http://localhost:5000/pending_tx'
fi


if [[ $1 == "MINE" ]]
then
  curl -GET 'http://localhost:5000/mine'
fi


if [[ $1 == "BLOCKCHAIN" ]]
then
  curl -GET 'http://localhost:5000/chain'
fi


if [[ $1 == "LASTBLOCK" ]]
then
  curl -GET 'http://localhost:5000/last_block'
fi
