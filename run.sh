#!/bin/bash

echo $PICKLED_TOKEN | base64 -d >token.pickle
echo $CREDENTIALS_JSON >credentials.json
pipenv install
pipenv run python main.py
git commit -am "committing spring-tips.xml at %s $(date +%s)"
