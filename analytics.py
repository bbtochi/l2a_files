## This is a python file

"""
* LEARN TO USE GIT ON THIS COMPUTER **DONE**
* CREATE DATA ANALYSIS REPOSITORY ON GIT AND GET SOME FILES **DONE**
* FIND OUT HOW TO GET ROUTE LENGTHS **DONE**
* FIND OUT DAYS OF WEEK **DONE**
* OUTPUT DISTANCES TO CSV FILE

"""
# READ IN DATA
from googlemaps import convert
from googlemaps.convert import as_list
import csv
import urllib
import simplejson
from time import sleep
from datetime import date

data_file = 'nytraffic.csv'
output_file = "output.csv"
data = []
origins = []
destinations = []
roadways = {}
distances = {}
weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

def density(length, flowrate):
    # estimate number of vehicles at any given minute
    vehicles = flowrate/60
    dty = vehicles/length
    print "Density: "+dty
    return dty

def weekday(day):
    """ day is mm/dd/yyyy """
    day = day.split("/")
    dt = date(int(day[2]),int(day[0]),int(day[1]))
    return weekdays[dt.isoweekday()-1]

def clean_row(row,i):
    while row[i][0] == " " or row[i][-1] == " ":
        if row[i][0] == " ":
            row[i] = row[i][1:]
        elif row[i][-1] == " ":
            row[i] = row[i][:-1]

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

googledistmatrixUrl = 'http://maps.googleapis.com/maps/api/distancematrix/json?'
incorrect = {"count": 0}

def get_distance(origins, destinations):
    params = {
        "origins": _convert_path(origins),
        "destinations": _convert_path(destinations)
    }
    url = googledistmatrixUrl + urllib.urlencode(params)
    json_response = urllib.urlopen(url)
    # print "HEEEEYYYYYY!!!!!!"
    # print json_response
    response = simplejson.loads(json_response.read())
    if response['status'] == "OK":
        for i in range(len(origins)):
            origin = response['origin_addresses'][i]
            destination = response['destination_addresses'][i]
            distance = response["rows"][i]["elements"][0]["distance"]["text"]
            distances[(origin,destination)] = distance

            dst = distance.split(" ")
            dt = float(dst[0])
            if dst[1] == "km" and dt > 3.:
                incorrect["count"] +=1
                print
                print "FROM: " + origin
                print "TO: " + destination
                # print distance
                print "wrong distance: "+distance
                # print

            return distance
    else:
        print "ERROR!"
        print response["status"]
        return response["status"]

def _convert_path(waypoints):
    # Handle the single-tuple case
    if type(waypoints) is tuple:
        waypoints = [waypoints]
    else:
        waypoints = as_list(waypoints)

    return convert.join_list("|",
            [(k if convert.is_string(k) else convert.latlng(k))
                for k in waypoints])


with open(data_file, 'r') as data_f:
    # Parse it as a CSV file.
    data_csv = csv.reader(data_f, delimiter=',', quotechar='"')

    # Skip the header row.
    next(data_csv, None)

    # Load the data.
    c = 0
    for row in data_csv:
        clean_row(row,2)
        clean_row(row,3)
        clean_row(row,4)
        dic = {'id':row[0], 'segid':row[1], 'roadname':row[2], 'from': row[3], 'to': row[4], 'direction': row[5], 'date': row[6]}

        # add in distance info
        roadway = dic["roadname"]
        if roadway in roadways:
            roadways[roadway]["count"]+=1
            dic["distance"] = roadways[roadway]["dist"]

        else:
            roadways[roadway] = {"dist": 0, "count": 1}
            o = row[2]+" and "+row[3]+", NY"
            d = row[2]+" and "+row[4]+", NY"
            origins.append(o)
            destinations.append(d)
            dic["distance"] = get_distance([o],[d])
            dist = dic["distance"].split(" ")
            dt = float(dist[0])
            if dist[1] == "km" and dt > 3.:
                print "should be..."
                print "FROM: " + o
                print "TO: " + d


        # add in day of week
        dic["day"] = weekday(dic["date"])
        c+=1

        # add in flow rates
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


print "INCORRECT #: ",incorrect["count"]
# o = [origins[0]]
# d = [destinations[0]]

# get_distance(["grand concourse serv and east 172 street, NY"],["grand concourse_serv and east mt eden avenue, NY"])

# GET COORDINATES OF UNIQUE ROUTES
# roadways = {}
# count = 0
# # loop through each row in data
# for entry in data:
#     roadway = entry["roadname"]
#     if roadway in roadways:
#         roadways[roadway]+=1
#     else:
#         count+=1
#         #print count
#         roadways[roadway] = 1
#         get_coordinates(entry["roadname"]+" and "+entry["from"])
#
#         sleep(0.5)
#         #print
#
# print "THERE ARE "+str(len(roadways))+" UNIQUE ROADWAYS"

# Write a prediction file.
with open(output_file, 'w') as outfile:

   # Produce a CSV file.
   out_csv = csv.writer(outfile, delimiter=',', quotechar='"', lineterminator = '\n')

   # Write the header row.
   out_csv.writerow(['Id', 'Prediction'])
   out_csv.writerow(['Id', 'Prediction'])
   # for i in range(10):
   #     out_csv.writerow(['w','w'])
