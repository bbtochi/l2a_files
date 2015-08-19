"""
* TEST THE GOOGLEMAPS DIRECTIONS CAPABILITIES
* FIND OUT HOW TO MAKE REQUESTS
* FIND OUT HOW TO INTERPRET RESULTS
* EXAMINE overview_path ARRAY OF LAT/LNG VALUES OUTLINING ROUTE
"""
from googlemaps import convert
from googlemaps.convert import as_list
import urllib
import simplejson

origins = ['800 market street, san francisco', 'sutter st and mason st, san francisco', 'post st and mason st, san francisco']
destinations = ['donwntown berkeley, CA', 'san jose, CA', 'Los Angeles, CA', '425 market street, san francisco']
start = origins[0]
stop = destinations[3]
googledirectionsUrl = 'http://maps.googleapis.com/maps/api/directions/json?'

# given a string, returns the coordinates of the location
def get_directions(origin, destination):
    params = {
        'origin': _convert_waypoint(origin),
        'destination': _convert_waypoint(destination)
    }
    url = googledirectionsUrl + urllib.urlencode(params)
    json_response = urllib.urlopen(url)
    response = simplejson.loads(json_response.read())
    if response['status'] == 'OK':
        # get waypointsg
        waypoints = response['geocoded_waypoints']
        # print "There are %d waypoints "%len(waypoints)
        # o = waypoints[0]
        # print o

        # get array of routes and the route we care about
        routes = response['routes']
        route = routes[0]
        print
        print "ROUTE"
        print "FROM: ",start
        print "TO: ",stop
        # print

        # get legs
        legs = route['legs']
        num_legs = len(legs)
        # if num_legs == 1:
        #     print "There is 1 leg"
        # else:
        #     print "There are %d legs"%num_legs
        # print

        # leg of interest
        i = 0
        leg = legs[i]
        steps = leg['steps']
        From = leg['start_address']
        To = leg['end_address']

        # print "LEGS"
        # print "Leg ",i
        # print "From: ",From
        # print "To: ",To
        print "has %d steps"%len(steps)
        print

        c = 1
        print "LAST %d STEPS"%c
        for i in range(1,c+1):
            i*= -1
            print "from %s to %s"%(steps[i]['start_location'],steps[i]['end_location'])
            print

    else:
        print "<no results>"

def _convert_waypoint(waypoint):
    if not convert.is_string(waypoint):
        return convert.latlng(waypoint)

    return waypoint
get_directions(start,stop)
