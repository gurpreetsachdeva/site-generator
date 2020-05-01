#!/bin/bash

echo $PICKLED_TOKEN | base64 -d >token.pickle
echo $CREDENTIALS_JSON >credentials.json
pipenv install
ls -la
du -hs token.pickle
du -hs credentials.json
pipenv run python main.py
git commit -am "committing spring-tips.xml at %s $( date +%s )"
