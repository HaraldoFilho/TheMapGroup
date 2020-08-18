#!/usr/bin/python3

# This script generates a html file of all the photos on the
# Flickr user's photostream, that can be viewed in a web browser as a map
#
# Author: Haraldo Albergaria
# Date  : Jul 21, 2020
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import flickrapi
import json
import os
import sys
import time
import math

from geopy.geocoders import Nominatim


# ================= CONFIGURATION VARIABLES =====================

# Limits
photos_per_page = '500'
max_number_of_pages = 200
max_number_of_photos = max_number_of_pages * int(photos_per_page)
max_number_of_markers = 5000

#geocoder
geo_accuracy = 0.001
geo_zoom = 18

# ===============================================================


# get full script's path
run_path = os.path.dirname(os.path.realpath(__file__))

# check if there is a api_credentials file and import it
if os.path.exists("{}/api_credentials.py".format(run_path)):
    import api_credentials
else:
    print("ERROR: File 'api_credentials.py' not found. Create one and try again.")
    sys.exit()

# Credentials
api_key = api_credentials.api_key
api_secret = api_credentials.api_secret

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# get geolocator
try:
    geolocator = Nominatim(user_agent="flickr_map")
except:
    print("ERROR: FATAL: Unable to get geolocator")
    sys.exit()


#===== FUNCTIONS ==============================================================#

# Function to get photo's geo privacy
def getGeoPrivacy(photo):
    if photo['geo_is_public'] == 1:
        return 1
    if photo['geo_is_contact'] == 1:
        return 2
    if photo['geo_is_friend'] == 1 and photo['geo_is_family'] == 0:
        return 3
    if photo['geo_is_friend'] == 0 and photo['geo_is_family'] == 1:
        return 4
    if photo['geo_is_friend'] == 1 and photo['geo_is_family'] == 1:
        return 5
    if photo['geo_is_friend'] == 0 and photo['geo_is_family'] == 0:
        return 6

# Function to verify if there is geo tag info
def isGeoTagged(photo):
    if photo['longitude'] != 0 and photo['latitude'] != 0:
        return True
    return False


#===== MAIN CODE ==============================================================#

# get group id from group url on config file
group_info = flickr.urls.lookupGroup(api_key=api_key, url='flickr.com/groups/the-map-group/')['group']
group_id = group_info['id']
group_name = group_info['groupname']['_content']

# stores the coordinates fo the markers
coordinates = []

# set script mode (photoset or photostream) and get the total number of photos
try:
    photos = flickr.groups.pools.getPhotos(api_key=api_key, group_id=group_id, privacy_filter='1', per_page=photos_per_page)
    npages = int(photos['photos']['pages'])
    total = int(photos['photos']['total'])
    print('Generating map for \'{}\''.format(group_name))
    print('{} photos in the pool'.format(total))
except:
    geolocator = None
    sys.exit()

# current number of photos on photostream
current_total = total

# difference on number of photos from previous run
delta_total = int(total)

# if there is no difference, finish script
if os.path.exists("{}/last_total.py".format(run_path)):
    import last_total
    delta_total = int(current_total) - int(last_total.number)
    if delta_total == 0:
        print('No changes on number of photos since last run.\nAborted.')
        geolocator = None
        sys.exit()

# if difference > 0, makes total = delta_total
# to process only the new photos, otherwise
# (photos were deleted), run in all
# photostream to update the entire map
if delta_total > 0:
    total = delta_total
    if total != delta_total:
        print('{} new photo(s)'.format(total))
else:
    n_deleted = abs(delta_total)
    print('{} photo(s) deleted from photostream.\nThe corresponding markers will also be deleted'.format(n_deleted))


print('Extracting photo coordinates and ids...')

# get number of pages to be processed
npages = math.ceil(total/int(photos_per_page))

# to be included on map
n_photos = 0  # counts number of photos
n_markers = 0 # counts number of markers

# extracts only the photos below a number limit
if npages > max_number_of_pages:
    npages = max_number_of_pages
    total = max_number_of_pages * int(photos_per_page);
    print("Extracting for the last {} photos".format(total))

# process each page
for pg in range(1, npages+1):

    page = flickr.groups.pools.getPhotos(api_key=api_key, group_id=group_id, privacy_filter='1', extras='geo,tags,url_sq', page=pg, per_page=photos_per_page)['photos']['photo']

    photos_in_page = len(page)

    # process each photo on page
    for ph in range(0, photos_in_page):

        photo = page[ph]

        # variable to store information if already exist a marker
        # on the same photo's coordinates
        marker_exists = False

        # check if photo can be included on the map (according to privacy settings)
        if True:

            n_photos += 1

            # get coordinates from photo
            longitude = float(photo['longitude'])
            latitude = float(photo['latitude'])
            photo_owner = photo['owner']

            # read each markers coordinates and append photo is case
            # there is already a marker on the same coordinate
            for coord in coordinates:
                if longitude == coord[0][0] and latitude == coord[0][1] and photo_owner == coord[1]:
                    coord[2].append([photo['id'], photo['url_sq']])
                    marker_exists = True
                    break

            # create a new marker to be added to the map
            if not marker_exists:
                coordinates.append([[longitude, latitude], photo_owner, [[photo['id'], photo['url_sq']]]])
                n_markers += 1

        # stop processing photos if any limit was reached
        if n_photos >= total or n_photos >= max_number_of_photos or n_markers >= max_number_of_markers:
           break

    print('Batch {0}/{1} | {2} photo(s) in {3} marker(s)'.format(pg, npages, n_photos, n_markers), end='\r')

    # stop processing pages if any limit was reached
    if n_photos >= total:
        break
    if n_photos >= max_number_of_photos:
        print("\nMaximum number of photos on map reached!", end='')
        break
    if n_markers >= max_number_of_markers:
        print("\nMaximum number of markers on map reached!", end='')
        break

# stop and exit script if there is no photo to be added to the map
if n_photos == 0:
    if mode == 'photoset':
        print('\nNo geo tagged photo on the user photoset\nMap not generated')
    else:
        print('\nNo geo tagged photo on the user photostream\nMap not generated')
    geolocator = None
    sys.exit()

print('\nAdding marker(s) to map...')

# check if there is javascript file with the markers on map already
# and readt it otherwise created a new one
if os.path.exists("{}/locations.js".format(run_path)):
    locations_js_file = open("{}/locations.js".format(run_path))
else:
    locations_js_file = open("{}/locations.js".format(run_path), 'w')
    locations_js_file.write("var locations = [\n")
    locations_js_file.write("]\n")
    locations_js_file.close()
    locations_js_file = open("{}/locations.js".format(run_path))

# read the file and store it
locations_js_lines = locations_js_file.readlines()
locations_js_file.close()

# create a python file with the existing markers,
# import it and delete it
locations_py_file = open("{}/locations.py".format(run_path), 'w')
locations_py_file.write("locations = [\n")
for i in range(1, len(locations_js_lines)):
    locations_py_file.write(locations_js_lines[i])
locations_py_file.close()

time.sleep(1)

from locations import locations
os.system("rm {}/locations.py".format(run_path))

# create a new javascript file to store new markers
locations_js_file = open("{}/locations.js".format(run_path), 'w')
locations_js_file.write("var locations = [\n")

# get the number of markers (locations) already on map
n_locations = len(locations)
if n_locations > 0:
    print('Map already has {} marker(s)'.format(n_locations))

# counts the number of new photos added to markers
new_photos = 0

# process each marker info already on map
for loc in range(n_locations):

    # get info for photos on marker
    photos_info = locations[loc][2]
    n_photos = int(locations[loc][3])

    # get number of photos (coordinates) to be added to map
    n_coords = len(coordinates)

    # iterate over each coordinate
    for coord in range(n_coords-1, -1, -1):

        # if there is already a marker on the same coordinate
        if coordinates[coord][0] == locations[loc][0]:

            photo_owner = locations[loc][1]

            # read each photo already on the marker
            for photo in coordinates[coord][2]:
                photo_id = photo[0]
                thumb_url = photo[1]

                # if the photo is not already on marker, add the photo to it
                if photo_id not in photos_info:
                    photos_info.append([photo_id, thumb_url])
                    new_photos += 1

            # remove photo info from
            # coordinates to be added
            coordinates.pop(coord)

    # update the number of photos on marker
    n_photos += new_photos
    locations[loc][1] = photos_info
    locations[loc][3] = n_photos
    locations_js_file.write("    {}".format(locations[loc]))

    if len(coordinates) > 0:
        locations_js_file.write(",\n")
    else:
        locations_js_file.write("\n")

if new_photos > 0:
    print('Added {} new photo(s) to existing markers'.format(new_photos))

# reverse the coordinates order so
# the newest ones go to the end
coordinates.reverse()

# check if there is remaining markers to be added
n_markers = len(coordinates)
if n_markers > 0:
    print('{} new marker(s) will be added to the map'.format(n_markers))

# remove the oldest locations to make
# room for new markers without violate
# the max number of markers limit
new_locations_length = len(locations) + n_markers
if new_locations_length >= max_number_of_markers:
    new_locations_length = max_number_of_markers - n_markers
    print('Max number of markers reached. Removing {} marker(s)...'.format(n_markers))
    while len(locations) > new_locations_length:
        locations.pop(0)

new_markers = 0

# iterate over each marker to be added
for marker_info in coordinates:

    new_markers += 1

    # get coordinates of the new marker
    longitude = float(marker_info[0][0])
    latitude = float(marker_info[0][1])
    photo_owner =  marker_info[1]

    # write it to locations file
    locations_js_file.write("    [[{0}, {1}], \'{2}\', [".format(longitude, latitude, photo_owner))

    # counts number of photos on marker
    n_photos = 0

    # iterate over each photo
    for i in range(len(marker_info[2])):

        # add photo to marker, writing it to locations file
        photo_id = marker_info[2][i][0]
        thumb_url =  marker_info[2][i][1]
        locations_js_file.write("[\'{0}\', \"{1}\"]".format(photo_id, thumb_url))
        if i < len(marker_info[2])-1:
            locations_js_file.write(", ")
        n_photos += 1

    # finish marker writing to location file
    locations_js_file.write("], {}]".format(n_photos))
    if new_markers < n_markers:
        locations_js_file.write(",\n")
    else:
        locations_js_file.write("\n")

    print('Added marker {0}/{1}'.format(new_markers, n_markers), end='\r')

# finish script
if new_markers > 0:
    print('')
else:
    print('No new markers were added to the map')

print('Finished!')

locations_js_file.write("]\n")
locations_js_file.close()

# update last_total file with the new value
if os.path.exists("{}/locations.js".format(run_path)):
    os.system("echo \"number = {0}\" > {1}/last_total.py".format(current_total, run_path))
