#!/bin/bash
cd google-sheet-ingest
git config --global user.email "josh@joshlong.com"
git config --global user.name "Spring Tips"
echo "$PICKLED_TOKEN" | base64 -d >token.pickle
echo "$CREDENTIALS_JSON" >credentials.json
pipenv install
FN=`pwd`/spring-tips.xml
pipenv run python main.py $FN
cd ..

output=$HOME/out
rm -rf $output
git clone https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/spring-tips/spring-tips.github.io.git $output
cp $FN $output/rss.xml
cd $output 
git add $output/rss.xml 
git commit -am "updated $FN @ $(date)"
git push