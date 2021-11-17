#!/bin/bash

PROJECT_NAME="$1.prdeploy.xyz"
REPO_LINK=$2
BRANCH_NAME=$3

mkdir /var/www/"$PROJECT_NAME"
cd /var/www/"$PROJECT_NAME"
mkdir temp

git clone "$REPO_LINK" temp
cd temp
git checkout "$BRANCH_NAME"

python3 -m venv "$PROJECT_NAME-$BRANCH_NAME-env"
source "$PROJECT_NAME-$BRANCH_NAME-env"/bin/activate

pip install -r requirements.txt

<<<<<<< HEAD
=======
# this can be replaced depending on what framework we are working on
>>>>>>> 6dedbd7c143007adb62a65195b3a441fe24c1081
mkdocs build

cd site

cp -r . /var/www/"$PROJECT_NAME"

cd /var/www/"$PROJECT_NAME"

rm -rf temp