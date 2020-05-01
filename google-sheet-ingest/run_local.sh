files=$HOME/Dropbox/spring-tips/spring-tips-sheet/secure/
export PICKLED_TOKEN=$(cat $files/token.pickle | base64)
export CREDENTIALS_JSON=$(cat $files/credentials.json)
FN=spring-tips.xml
pipenv run python main.py $FN
git pull
git add $FN
git commit -am "committing $FN at $( date )"
git push