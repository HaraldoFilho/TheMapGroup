#!/bin/bash

RUN_DIR="/home/pi/flickr_map/groups"
REPO_DIR="/home/pi/github/the-map-group.github.io"
GRP_DIR="groups"
MAP_GRP="the-map-group"
EFS_10="efs-at10mm"
EFS_250="efs-at250mm"
MAP_FILE="index.html"

$RUN_DIR/$MAP_GRP/generate-map.py
$RUN_DIR/$EFS_10/generate-map.py
$RUN_DIR/$EFS_250/generate-map.py

DIFF_MAP=$(git diff $REPO_DIR/$MAP_FILE)
DIFF_10=$(git diff $REPO_DIR/$GRP_DIR/$EFS_10/$MAP_FILE)
DIFF_250=$(git diff $REPO_DIR/$GRP_DIR/$EFS_250/$MAP_FILE)

if [[ ! -z $DIFF_MAP ]] || [[ ! -z $DIFF_10 ]] || [[ ! -z $DIFF_250 ]];
    then
        cd $REPO_DIR
        git pull origin master
        git add *
        git commit -m "Updated Maps"
        git push origin master
#        git push fork master
    else
       echo "Maps not updated. No differences from previous version."
fi

exit 0
