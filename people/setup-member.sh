#!/bin/bash

mkdir /home/pi/github/the-map-group.github.io/people/$1
cd /home/pi/github/the-map-group.github.io/people/$1
ln -s ../../api_credentials.py .
ln -s ../../mapbox_token .
ln -s ../../statcounter .
ln -s /home/pi/flickr_map/header.html .
ln -P /home/pi/flickr_map/generate-map.py
echo "user = '$1'" > config.py
echo "photoset_id = ''" >> config.py
echo "photo_privacy = 1" >> config.py
echo "geo_privacy = 1" >> config.py
echo "dont_map_tag = 'DontMap'" >> config.py

