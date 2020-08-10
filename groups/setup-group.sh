#!/bin/bash

REPO_DIR="/home/pi/github/the-map-group.github.io"
GEN_MAP_DIR="/home/pi/flickr_map"

if [[ -e $REPO_DIR/groups/$1 ]];
    then
        rm -fr $REPO_DIR/groups/$1
fi

mkdir $REPO_DIR/groups/$1
cd $REPO_DIR/groups/$1
ln -s ../../api_credentials.py .
ln -s ../../mapbox_token .
ln -s ../../statcounter .
ln -s $GEN_MAP_DIR/groups/map.html .
ln -P $GEN_MAP_DIR/groups/generate-map.py
echo "# group alias or id" > config.py
echo "group = '$1'" >> config.py
