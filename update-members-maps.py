#!/usr/bin/python3

# Author: Haraldo Albergaria
# Date  : Jul 29, 2020
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


import flickrapi
import api_credentials
import importlib
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


#===== FUNCTIONS ==============================================================#

def memberFilesExist(member_path):
    locations_exists = os.path.exists("{}/locations.py".format(member_path))
    countries_exists = os.path.exists("{}/countries.py".format(member_path))
    user_exists = os.path.exists("{}/user.py".format(member_path))
    if locations_exists and countries_exists and user_exists:
        return True
    return False


#===== MAIN CODE ==============================================================#

# create members list file
members_file = open("{}/members_list".format(people_path), 'w')

# create members info file
members_js_file = open("{}/members.js".format(repo_path), 'w')
members_js_file.write("var members = [\n")

# get group id and name from group url
try:
    group_id = flickr.urls.lookupGroup(api_key=api_key, url=group_url)['group']['id']
    group_name = flickr.groups.getInfo(group_id=group_id)['group']['name']['_content']
except:
    sys.exit()

# get members from group
try:
    members = flickr.groups.members.getList(api_key=api_key, group_id=group_id)
    total_of_members = int(members['members']['total'])
    number_of_pages  = int(members['members']['pages'])
    members_per_page = int(members['members']['perpage'])
except:
    sys.exit()

if os.path.exists("{}/countries/members.py".format(repo_path)):
    os.system("rm {}/countries/members.py".format(repo_path))

# iterate over each members page
for page_number in range(number_of_pages, 0, -1):

    try:
        members = flickr.groups.members.getList(api_key=api_key, group_id=group_id, page=page_number, per_page=members_per_page)['members']['member']
    except:
        sys.exit()

    # iterate over each member in page
    for member_number in range(len(members)-1, -1, -1):
        try:
            member_name = members[member_number]['username']
            member_id = members[member_number]['nsid']
            member_alias = flickr.people.getInfo(api_key=api_key, user_id=member_id)['person']['path_alias']
            if member_alias == None:
                member_alias = member_id
            member_path = people_path + "/" + member_alias

            # create member directory and topic if doesn't exist yet
            is_new_member = False
            if not os.path.isdir(member_path):
                command = "{0}/setup-member.sh {1}".format(people_path, member_alias)
                os.system(command)
                is_new_member = True

            if is_new_member:
                print('##### Generating map for new member: {}...'.format(member_name[0:16]))
            else:
                print('##### Updating map for member: {}...'.format(member_name[0:20]))
                # get 'locations.py', 'countries.py' and 'user.js' from github
                print('Getting locations and countries from remote...')
                try:
                    if not os.path.exists("{}/locations.py".format(member_path)):
                        command = "wget -q -P {0} https://raw.githubusercontent.com/the-map-group/the-map-group.github.io/master/people/{1}/locations.py".format(member_path, member_alias)
                        os.system(command)
                    if not os.path.exists("{}/countries.py".format(member_path)):
                        command = "wget -q -P {0} https://raw.githubusercontent.com/the-map-group/the-map-group.github.io/master/people/{1}/countries.py".format(member_path, member_alias)
                        os.system(command)
                    if not os.path.exists("{}/user.py".format(member_path)):
                        command = "wget -q -P {0} https://raw.githubusercontent.com/the-map-group/the-map-group.github.io/master/people/{1}/user.py".format(member_path, member_alias)
                        os.system(command)
                except:
                    pass

            if not is_new_member and not memberFilesExist(member_path):
                continue

            if memberFilesExist(member_path):
                prev_loc_fsize = os.stat("{}/locations.py".format(member_path)).st_size
            else:
                prev_loc_fsize = 0

            # generate/update member's map
            print('Starting \'Flickr Map\' script...')
            command = "{}/generate-map-data.py".format(member_path)
            os.system(command)

            if memberFilesExist(member_path):
                loc_fsize_diff = os.stat("{}/locations.py".format(member_path)).st_size - prev_loc_fsize
            else:
                loc_fsize_diff = 0

            # updates countries members file
            if memberFilesExist(member_path):
                command = "{}/update-countries-map-data.py".format(member_path)
                os.system(command)

            # upload map
            if (loc_fsize_diff != 0 or is_new_member) and memberFilesExist(member_path):
                print('Uploading map data...')
                os.system("git pull -q origin master")
                os.system("git add -f {}/index.html".format(member_path))
                os.system("git add -f {}/locations.py".format(member_path))
                os.system("git add -f {}/countries.py".format(member_path))
                os.system("git add -f {}/user.py".format(member_path))
                os.system("git commit -m \"Updated map for member \'{}\'\"".format(member_name))
                os.system("git push -q origin master")
                print('Done!')
            else:
                print("Everything is up-to-date. Nothing to upload!")

            if is_new_member:
                topic_subject = "[MAP] {}".format(member_name)
                member_map = "{0}/people/{1}/".format(map_group_url, member_alias)
                topic_message = "[{0}/{1}/] Map link: <a href=\"{3}\"><b>{3}</b></a>\n\nClick on the markers to see the photos taken on the corresponding location.".format(photos_url, member_alias, member_name, member_map)
                flickr.groups.discuss.topics.add(api_key=api_key, group_id=group_id, subject=topic_subject, message=topic_message)
                print('Created discussion topic for new member')
        except:
            pass

        # get member information
        print("Getting member information...")

        os.system("cp {0}/user.py {1}/".format(member_path, repo_path))
        import user
        importlib.reload(user)
        from user import user_info
        os.system("rm {}/user.py".format(repo_path))

        member_name = user_info['name']
        if len(member_name) > 30:
            member_name = member_name[:30]

        member_avatar = "\"{}\"".format(user_info['avatar'].replace('../../', ''))

        member_n_places = user_info['markers']
        member_n_photos = user_info['photos']

        if os.path.exists("{}/locations.py".format(member_path)):
            os.system("rm {}/locations.py".format(member_path))
        if os.path.exists("{}/countries.py".format(member_path)):
            os.system("rm {}/countries.py".format(member_path))
        if os.path.exists("{}/user.py".format(member_path)):
            os.system("rm {}/user.py".format(member_path))
        os.system("rm -fr {}/__pycache__".format(member_path))

        members_file.write("{}\n".format(member_alias))

        members_js_file.write("  [\'{0}\', \'{1}\', \'{2}\', {3}, {4}, {5}".format(member_id, member_alias, member_name, member_avatar, member_n_places, member_n_photos))
        if member_number > 0:
            members_js_file.write("],\n")
        else:
            members_js_file.write("]\n")
        print("Finished!\n")

members_file.close()

members_js_file.write("]\n")
members_js_file.close()

if os.path.exists("{}/countries/members.py".format(repo_path)):
    os.system("git pull -q origin master")
    os.system("git add -f {}/countries/*".format(repo_path))
    os.system("git commit -m \"Updated countries members files\"")
    os.system("git push -q origin master")

