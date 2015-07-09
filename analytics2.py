"""
* READ IN DATA WITH SPEED ESTIMATES FOR EACH HOUR BLOCK
* PREDICT SPEED INFO FOR EACH ROUTE ON SPECIFIC DAYS
"""

"""
OUTPUT FORMAT
{
    (From_A,To_B): {
        "Monday": {24:00-1:00: 2m/h, 1:00-2:00: 3m/h, ...}
        "Tuesday": ...
    },
    (From_A,To_B): {
        "Monday": {24:00-1:00: 2m/h, 1:00-2:00: 3m/h, ...}
        "Tuesday": ...
    }
}

FORMAT TO PERFORM CALCULATION
{
    (From_A,To_B): {
        "Monday": {"count": 10, "24:00-1:00": 50, "1:00-2:00": 10, ...}
        "Tuesday": ...
    },
    (From_A,To_B): {
        "Monday": {"count": 10, "24:00-1:00": 50, "1:00-2:00": 10, ...}
        "Tuesday": ...
    }
}
"""

import csv
import json

in_file = "speed_estimates"
out_file = "results"
routes = {}
week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

# read in data
with open(in_file, 'r') as in_f:
    # parse as csv file
    in_csv = csv.reader(in_f, delimiter=',', quotechar='"')

    # skip header
    next(in_csv,None)

    for entry in in_csv:
        # assign some useful entry info to variables
        route, dr, dst, dt, day = entry[1]+","+entry[2], entry[3], entry[4], entry[5], entry[6]

        # update speed info for specific day
        i,j = 24,1
        while j != 25:
            time = str(i)+':00-'+str(j)+':00'
            speed = float(entry[j+6])

            #check route has been seen
            if route not in routes:
                routes[route] = {day: {}}
                routes[route][day][time] = speed
                routes[route][day]["count"] = 1.0
            # check if day has been seen for route
            elif day not in routes[route]:
                routes[route][day] = {"count": 1.0, time: speed}
            # check if time has been seen on this day of week for this route
            elif time not in routes[route][day]:
                routes[route][day][time] = speed
            else:
                routes[route][day][time]+= speed
            i=j
            j+=1

        routes[route][day]["count"]+= 1.0

incomplete = 0
for route in routes:
    # print route
    info = {}
    for day in routes[route]:
        # info[day] = routes[route][day]["count"]
        for time in routes[route][day]:
            if routes[route][day]["count"]!=1.:
                routes[route][day][time] /= routes[route][day]["count"]
    # print info
    # print
    if len(info) < 7:
        incomplete+=1

print "THERE ARE %d ROUTES OUT OF %d WITHOUT A FULL WEEK'S DATA"%(incomplete,len(routes))
with open(out_file, 'w') as out_f:
    json.dump(routes, out_f, indent=8)
