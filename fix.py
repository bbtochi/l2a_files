"""
* GET CORRECT FROM AND TO ADDRESSES FROM OLD FILE AND CORRECT THEM IN RIGH DISTANCES
"""

from googlemaps import convert
from googlemaps.convert import as_list
import csv
import urllib
import simplejson
from datetime import date

data_file = 'fix.csv'
output_file = "new1.csv"
# https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452
googleRevGeocodeUrl = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='
seen = {}


def get_address(query):
    query = query[1:-1]

    # if already been queried, return address
    if query in seen:
        return seen[query]
    else:
        query = query.encode('utf-8')
        url = googleRevGeocodeUrl + query
        json_response = urllib.urlopen(url)
        response = simplejson.loads(json_response.read())
        if response['results']:
            address = response['results'][0]['formatted_address']
            seen[query] = address
            print "ADDRESS: ", address
            print
            return address
        else:
            latitude, longitude = None, None
            print query + ": ", "<no results>"
            return

# get_address('(40.714224,-73.961452)')

# read in correct latlng locations from fix.csv file
with open(data_file, 'r') as fix_f:
    fix_csv = csv.reader(fix_f, delimiter=',', quotechar='"')

    # skip header
    next(fix_csv,None)

    # have array for output data
    data = []

    for row in fix_csv:
        if int(row[1]) > 355:
            entry = {}
            entry['id'] = row[1]
            entry['from'] = get_address(row[2])
            entry['to'] = get_address(row[3])
            data.append(entry)

# write correct addresses to outfile
with open(output_file, 'w') as out_f:
    out_csv = csv.writer(out_f, delimiter=',', quotechar='"', lineterminator = '\n')

    header = ["ID","FROM","TO"]
    out_csv.writerow(header)

    for entry in data:
        row = [entry['id'],entry['from'],entry['to']]
        out_csv.writerow(row)
