files=$HOME/Dropbox/spring-tips/spring-tips-sheet/secure/
export PICKLED_TOKEN=$(cat $files/token.pickle | base64)
export CREDENTIALS_JSON=$(cat $files/credentials.json)
pipenv run python main.py
git pull
git add spring
git commit -am "committing spring-tips.xml at %s $( date +%s )"
git push