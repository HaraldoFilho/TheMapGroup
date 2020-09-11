#!/bin/bash

REPO_DIR="/home/pi/github/the-map-group.github.io"
GEN_MAP_DIR="/home/pi/flickr_map"

if [[ -e $REPO_DIR/people/$1 ]];
    then
        rm -fr $REPO_DIR/people/$1
fi

mkdir $REPO_DIR/people/$1
cd $REPO_DIR/people/$1
ln -s ../../api_credentials.py .
ln -s ../../mapbox_token.py .
ln -s ../../countries_info.py .
ln -s ../../countries/members.py countries_members.py
ln -P $GEN_MAP_DIR/generate-map-data.py .
ln -P ../index.html .
ln -P ../update-countries-map-data.py .
echo "user = '$1'" > config.py
echo "photoset_id = ''" >> config.py
echo "photo_privacy = 1" >> config.py
echo "geo_privacy = 1" >> config.py
echo "dont_map_tag = 'DontMap'" >> config.py

