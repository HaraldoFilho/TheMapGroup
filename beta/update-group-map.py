#!/usr/bin/python3

# Author: Haraldo Albergaria
# Date  : Jul 29, 2020
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


import flickrapi
import api_credentials
import json
import time
import os
import sys


#===== CONSTANTS =================================#

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

group_url = "https://www.flickr.com/groups/the-map-group/"
photos_url = "http://www.flickr.com/photos"
map_group_url = "https://the-map-group.pictures"

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# get full script's path
repo_path = os.path.dirname(os.path.realpath(__file__))
people_path = repo_path + "/people"


#===== MAIN CODE ==============================================================#

print('##### Updating group map...')
# get 'locations.py' and 'members.js' from github
print('Getting locations and members from remote...')
try:
    if not os.path.exists("{}/locations.py".format(repo_path)):
        command = "wget -q -P {} https://raw.githubusercontent.com/the-map-group/the-map-group.github.io/master/locations.py".format(repo_path)
        os.system(command)
    if not os.path.exists("{}/members.js".format(repo_path)):
        command = "wget -q -P {} https://raw.githubusercontent.com/the-map-group/the-map-group.github.io/master/members.js".format(repo_path)
        os.system(command)
except:
    pass

# update group map
if os.path.exists("{}/last_total.py".format(repo_path)):
    os.system("rm {}/last_total.py".format(repo_path))
command = "{}/generate-map-data.py".format(repo_path)
os.system(command)
print('Uploading map data...')
os.system("git add -f {}/locations.py".format(repo_path))
os.system("git add -f {}/members.js".format(repo_path))
os.system("git commit -m \"Updated group map\"")
os.system("git push -q origin master")
print('Done!')
os.system("rm {}/locations.py".format(repo_path))
os.system("rm {}/members.js".format(repo_path))
os.system("rm -fr {}/__pycache__".format(repo_path))
