#!/bin/bash

REPO_DIR="/home/pi/github/the-map-group.github.io"

git pull origin master

cd $REPO_DIR/people/$1

./generate-map-data.py

git add countries.py
git add locations.py
git add user.py
git commit -m "Updated map for member '$1'"
git push origin master

rm countries.py
rm locations.py
rm user.py
