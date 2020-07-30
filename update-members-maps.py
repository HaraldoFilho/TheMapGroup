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
map_url = "https://the-map-group.pictures"

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# get full script's path
repo_path = os.path.dirname(os.path.realpath(__file__))
groups_path = repo_path + "/groups"
people_path = repo_path + "/people"


#===== MAIN CODE ==============================================================#

# get group id and name from group url
group_id = flickr.urls.lookupGroup(api_key=api_key, url=group_url)['group']['id']
group_name = flickr.groups.getInfo(group_id=group_id)['group']['name']['_content']

# get members from group
members = flickr.groups.members.getList(api_key=api_key, group_id=group_id)
total_of_members = int(members['members']['total'])
number_of_pages  = int(members['members']['pages'])
members_per_page = int(members['members']['perpage'])

# iterate over each members page
for page_number in range(1, number_of_pages+1):
    members = flickr.groups.members.getList(api_key=api_key, group_id=group_id, page=page_number, per_page=members_per_page)
    # iterate over each member in page
    for member_number in range(members_per_page):
        try:
            member_name = members['members']['member'][member_number]['username']
            member_id = members['members']['member'][member_number]['nsid']
            try:
                member_alias = flickr.people.getInfo(api_key=api_key, user_id=member_id)['person']['path_alias']
            except:
                member_alias = member_id
            member_path = people_path + "/" + member_alias
            # create member directory and topic if doesn't exist yet
            if not os.path.isdir(member_path):
                command = "{0}/setup-user.sh {1}".format(people_path, member_alias)
                os.system(command)
                topic_subject = "{}'s Map".format(member_name)
                map_url = "{0}/people/{1}/".format(map_url, member_alias)
                topic_message = "[{0}/{1}/]<a href=\"{0}/{1}/\"><b>{2}</b></a>\'s Map: <a href=\"{3}\"><b>{3}</b></a>".format(photos_url, member_alias, member_name, map_url)
                flickr.groups.discuss.topics.add(api_key=api_key, group_id=group_id, subject=topic_subject, message=topic_message)
            # generate/update member's map
            command = "{0}/generate_map.py".format(member_path)
            os.system(member_path + '/generate-map.py')
        except:
            pass

