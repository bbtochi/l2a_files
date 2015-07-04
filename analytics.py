## This is a python file

"""
* LEARN TO USE GIT ON THIS COMPUTER **DONE**
* CREATE DATA ANALYSIS REPOSITORY ON GIT AND GET SOME FILES **DONE**
* FIND OUT HOW TO GET ROUTE LENGTHS

"""
# READ IN DATA
import csv
import numpy as np
import urllib
import simplejson
from time import sleep

data_file = 'nytraffic.csv'
data = []
def clean_row(row,i):
    while row[i][0] == " " or row[i][-1] == " ":
        if row[i][0] == " ":
            row[i] = row[i][1:]
        elif row[i][-1] == " ":
            row[i] = row[i][:-1]

with open(data_file, 'r') as data_f:

    # Parse it as a CSV file.
    data_csv = csv.reader(data_f, delimiter=',', quotechar='"')

    # Skip the header row.
    next(data_csv, None)

    # Load the data.
    for row in data_csv:
        clean_row(row,2)
        clean_row(row,3)
        clean_row(row,4)
        dic = {'id':row[0], 'segid':row[1], 'roadname':row[2], 'from': row[3], 'to': row[4], 'direction': row[5], 'date': row[6]}
        i = 24
        j = 1
        count = 24
        while count != 0:
            key = str(i)+'-'+str(j)
            dic[key] = row[j+6]
            i=j
            j+=1
            count-=1
        data.append(dic)

googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'

def get_coordinates(query, from_sensor=False):
    query = query.encode('utf-8')
    params = {
        'address': query,
        'sensor': "true" if from_sensor else "false"
    }
    url = googleGeocodeUrl + urllib.urlencode(params)
    json_response = urllib.urlopen(url)
    response = simplejson.loads(json_response.read())
    if response['results']:
        location = response['results'][0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']
        print query + ": ", latitude, longitude
    else:
        latitude, longitude = None, None
        print query + ": ", "<no results>"
    return latitude, longitude

# count number of unique roadways
roadways = {}
count = 0
for i in range(len(data)):
    roadway = data[i]["roadname"]
    if roadway in roadways:
        roadways[roadway]+=1
    else:
        count+=1
        #print count
        roadways[roadway] = 1
        get_coordinates(data[i]["roadname"]+" and "+data[i]["from"])
        sleep(0.5)
        #print

print "THERE ARE "+str(len(roadways))+" UNIQUE ROADWAYS"

# get_coordinates("SPRING STREET and BROADWAY")
# a = [1,2,3]
# print a[-1]
