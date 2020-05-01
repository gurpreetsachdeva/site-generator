#!/bin/bash

git config --global user.email "josh@joshlong.com"
git config --global user.name "Spring Tips"
echo "$PICKLED_TOKEN" | base64 -d >token.pickle
echo "$CREDENTIALS_JSON" >credentials.json
pipenv install
FN=spring-tips.xml
pipenv run python main.py $FN
git pull
git add $FN
git commit -am "committing $FN at $(date)"
git push
