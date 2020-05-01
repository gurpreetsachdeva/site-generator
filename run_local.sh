cd google-sheet-ingest
files=$HOME/Dropbox/spring-tips/spring-tips-sheet/secure/
export PICKLED_TOKEN=$(cat $files/token.pickle | base64)
export CREDENTIALS_JSON=$(cat $files/credentials.json)

echo "$PICKLED_TOKEN" | base64 -d >token.pickle
echo "$CREDENTIALS_JSON" >credentials.json


FN=`pwd`/spring-tips.xml
pipenv install 
pipenv run python main.py $FN

rm token.pickle 
rm credentials.json 

cd ..
source $files/git.sh 


## TODO 
## take the XML file and then clone the 
## site generator github pages repo and add 
## it to that repo then commit changes

output=$HOME/Desktop/out
rm -rf $output

git clone https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/spring-tips/spring-tips.github.io.git $output 
cp $FN $output/rss.xml
cd $output 
git add $output/rss.xml 
git commit -am "updated $FN @ $(date)"
git push