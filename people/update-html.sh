#!/bin/bash

REPO_DIR="/home/pi/github/the-map-group.github.io"

if [[ -e $REPO_DIR/people/$1/index.html ]];
    then
        rm $REPO_DIR/people/$1/index.html
fi

cd $REPO_DIR/people/$1
ln -P ../index.html .
