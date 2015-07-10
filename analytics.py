"""
* LEARN TO USE GIT ON THIS COMPUTER **DONE**
* CREATE DATA ANALYSIS REPOSITORY ON GIT AND GET SOME FILES **DONE**
* FIND OUT HOW TO GET ROUTE LENGTHS **DONE**
* FIND OUT DAYS OF WEEK **DONE**
* OUTPUT DISTANCES TO CSV FILE **DONE**
"""
from googlemaps import convert
from googlemaps.convert import as_list
import csv
import urllib
import simplejson
from datetime import date

data_file = 'nytraffic.csv'
output_file = "output.csv"
data = []
times = []
# roadways = {}
routes = {}
distances = {}
weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'
googledistmatrixUrl = 'http://maps.googleapis.com/maps/api/distancematrix/json?'
incorrect = {"count": 0}

# given a date, returns the day of week
def weekday(day):
    """ day is mm/dd/yyyy """
    day = day.split("/")
    dt = date(int(day[2]),int(day[0]),int(day[1]))
    return weekdays[dt.isoweekday()-1]

# removes leading and trailing spaces in a string
def clean_row(row,i):
    while row[i][0] == " " or row[i][-1] == " ":
        if row[i][0] == " ":
            row[i] = row[i][1:]
        elif row[i][-1] == " ":
            row[i] = row[i][:-1]

# given a string, returns the coordinates of the location
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
    else:
        latitude, longitude = None, None
        print query + ": ", "<no results>"
    return latitude, longitude

# returns the distance between two locations
def get_distance(origins, destinations):
    params = {
        "origins": _convert_path(origins),
        "destinations": _convert_path(destinations)
    }
    url = googledistmatrixUrl + urllib.urlencode(params)
    json_response = urllib.urlopen(url)
    response = simplejson.loads(json_response.read())
    if response['status'] == "OK":
        for i in range(len(origins)):
            origin = response['origin_addresses'][i]
            destination = response['destination_addresses'][i]
            distance = response["rows"][i]["elements"][0]["distance"]["text"]
            distances[(origin,destination)] = distance

            dst = distance.split(" ")
            dt = float(dst[0])
            # if distance is too large or too small
            if (dst[1] == "km" and dt > 3.) or (dst[1] == "m" and dt < 4.):
                incorrect["count"] +=1
                print
                print "FROM: " + origin
                print "TO: " + destination
                print "wrong distance: "+distance
            return distance
    else:
        print "ERROR!"
        print response["status"]
        return response["status"]

# helper function that converts the input into the correct format
def _convert_path(waypoints):
    # Handle the single-tuple case
    if type(waypoints) is tuple:
        waypoints = [waypoints]
    else:
        waypoints = as_list(waypoints)

    return convert.join_list("|",
            [(k if convert.is_string(k) else convert.latlng(k))
                for k in waypoints])

# pairings = []
# entry_count = 0
# previous = "None"
# ewos = 0

# READ IN NY FILE
with open(data_file, 'r') as data_f:
    # Parse it as a CSV file.
    data_csv = csv.reader(data_f, delimiter=',', quotechar='"')

    # Skip the header row.
    next(data_csv, None)

    # Load the data.
    # go through each entry in the data
    for row in data_csv:
        # entry_count+=1

        # get rid of leading and trailing spaces in input
        clean_row(row,2)
        clean_row(row,3)
        clean_row(row,4)
        dic = {'id':row[0], 'segid':row[1], 'roadname':row[2], 'from': row[3], 'to': row[4], 'direction': row[5], 'date': row[6], 'wrong_dist': False}

        # add in day of week
        dic["day"] = weekday(dic["date"])

        # assign origin and destination information
        o = row[2]+" and "+row[3]+", NY"
        d = row[2]+" and "+row[4]+", NY"
        route = dic["roadname"]
        # if p not in pairings:
        #     pairings.append(p)

        #add in distance coordinates info
        # roadway = dic["roadname"]
        # if roadway != previous and previous!= "None":
        #     roadways[previous]["done"] = True

        # previous = roadway
        # if roadway in roadways:
        if route in routes:
            # if roadways[roadway]["done"]==True:
            #     print roadway
            #     ewos+=1
            #     print "ewo! ",ewos
            routes[route]["count"]+=1
            dic["distance"] = routes[route]["dist"]
            dic["origin"] = routes[route]["origin"]
            dic["destination"] = routes[route]["destination"]
        else:
            routes[route] = {"dist": 0, "count": 1, "origin": o, "destination": d, "done": False}
            routes[route]["dist"] = dic["distance"] = get_distance([o],[d])
            routes[route]["origin"] = dic["origin"] = get_coordinates(o)
            routes[route]["destination"] = dic["destination"] = get_coordinates(d)

            # check if distance is too large or too small
            dist = dic["distance"].split(" ")
            # fix distance unit error
            if len(dic['distance'].split(" ")) == 1:
                print dist[0]
                dic["distance"] = dic["distance"][:-1]+" m"
            dt = float(dist[0])
            if (dist[1] == "km" and dt > 3.) or (dist[1] == "m" and dt < 4.):
                dic["wrong_dist"] = True
                print "should be..."
                print "FROM: " + o
                print "TO: " + d

        # add in flow rates
        i = 24
        j = 1
        while j != 25:
            key = str(i)+'-'+str(j)
            if key not in times:
                times.append(key)
            dic[key] = row[j+6]
            i=j
            j+=1
        data.append(dic)

print "INCORRECT #: ",incorrect["count"]
# print "output: ",len(roadways)
# print len(pairings)

# Write distances to output file.
with open(output_file, 'w') as outfile:

   # Produce a CSV file.
   out_csv = csv.writer(outfile, delimiter=',', quotechar='"', lineterminator = '\n')

   # Write the header row.
   out_csv.writerow(['Incorrect Distance','ID',"ORIGIN","DESTINATION","DIR","DISTANCE","DATE","DAY"]+times)

   for entry in data:
       # get flow rates info for each entry
       frs = []
       for time in times:
           frs.append(entry[time])

       # write row to file
       row = [entry["wrong_dist"],entry["id"],entry["origin"],entry["destination"],entry["direction"],entry["distance"],entry["date"],entry["day"]]+frs
       out_csv.writerow(row)
