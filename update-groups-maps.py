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
groups_url = "https://www.flickr.com/groups"
photos_url = "http://www.flickr.com/photos"
map_url = "https://the-map-group.pictures"

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# get full script's path
repo_path = os.path.dirname(os.path.realpath(__file__))
groups_path = repo_path + "/groups"

group_tag = '[GROUP] '


#===== FUNCTIONS ==============================================================#

def updateGroup(map_group_alias):
    try:
        map_group_url = "{0}/{1}".format(groups_url, map_group_alias)
        map_group_id = flickr.urls.lookupGroup(api_key=api_key, url=map_group_url)['group']['id']
        map_group_info = flickr.groups.getInfo(api_key=api_key, group_id=map_group_id)['group']
        map_group_name = map_group_info['name']['_content']
        map_group_path = groups_path + "/" + map_group_alias
        # create group directory if doesn't exist yet
        is_new_group = False
        if not os.path.isdir(map_group_path):
            command = "{0}/setup-group.sh {1}".format(groups_path, map_group_alias)
            os.system(command)
            is_new_group = True
        # generate/update group's map
        command = "{}/generate-map.py".format(map_group_path)
        os.system(command)
        if os.path.exists("{}/map.html".format(map_group_path)) and os.path.exists("{}/statcounter".format(map_group_path)):
            map_file = open("{}/map.html".format(map_group_path))
            map = map_file.readlines()
            map_file.close()
            stats_file = open("{}/statcounter".format(map_group_path))
            stats = stats_file.readlines()
            stats_file.close()
            index_file = open("{}/index.html".format(map_group_path), 'w')
        else:
            sys.exit()

        for map_line in map:
            if map_line == "</body>\n":
                for stats_line in stats:
                    index_file.write(stats_line)
                index_file.write('\n')
            index_file.write(map_line)
        index_file.close()

        # upload map
        if os.path.exists("{}/index.html".format(map_group_path)):
            if map_group_alias == 'the-map-group':
                os.system("cp {0}/index.html {1}".format(map_group_path, repo_path))
                os.system("git add -f {}/index.html".format(repo_path))
            else:
                os.system("git add -f {}/index.html".format(map_group_path))
            os.system("git commit -m \"Updated map for group \'{}\'\"".format(map_group_name))
            os.system("git push origin master")
            print('Uploaded map')
            os.system("rm {}/map.html".format(map_group_path))
            os.system("rm {}/index.html".format(map_group_path))
            if is_new_group:
                reply_message = "Group map link: {0}/groups/{1}/".format(map_url, map_group_alias)
                flickr.groups.discuss.replies.add(api_key=api_key, group_id=map_group_id, topic_id=topic_id, message=reply_message)
                print('Replied with the link for the new group')
    except:
        pass


#===== MAIN CODE ==============================================================#

# get group id and name from group url
group_id = flickr.urls.lookupGroup(api_key=api_key, url=group_url)['group']['id']
group_name = flickr.groups.getInfo(group_id=group_id)['group']['name']['_content']

# get topics from group
topics = flickr.groups.discuss.topics.getList(api_key=api_key, group_id=group_id)
total_of_topics = int(topics['topics']['total'])
number_of_pages  = int(topics['topics']['pages'])
topics_per_page = int(topics['topics']['per_page'])

# iterate over each members page
for page_number in range(1, number_of_pages+1):
    topics = flickr.groups.discuss.topics.getList(api_key=api_key, group_id=group_id, page=page_number, per_page=topics_per_page)['topics']
    # iterate over each member in page
    for topic_number in range(len(topics['topic'])):
        try:
            topic_item = topics['topic'][topic_number]
            topic_subject = topic_item['subject']
            topic_id = topic_item['id']
            if group_tag in topic_subject:
                map_group_alias = topic_item['message']['_content']
                updateGroup(map_group_alias)
        except:
           pass

updateGroup('the-map-group')

if os.path.exists("{}/index.html".format(repo_path)):
    os.system("rm {}/index.html".format(repo_path))

