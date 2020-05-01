#!/bin/bash

pipenv install
echo $PICKLED_TOKEN | base64 -d > token.pickle
echo $CREDENTIALS_JSON   > credentials.json
ls -la
du -hs token.pickle
du -hs credentials.json
pipenv run python sheets.py
