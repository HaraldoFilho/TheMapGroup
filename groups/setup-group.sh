#!/bin/bash

mkdir /home/pi/github/the-map-group.github.io/groups/$1
cd /home/pi/github/the-map-group.github.io/groups/$1
ln -s ../../api_credentials.py .
ln -s ../../mapbox_token .
ln -s ../../statcounter .
ln -s /home/pi/flickr_map/header.html .
ln -P /home/pi/flickr_map/groups/generate-map.py
echo "# group alias or id" > config.py
echo "group = '$1'" >> config.py
