"""
* READ IN DATA WITH SPEED ESTIMATES FOR EACH HOUR BLOCK
* PREDICT SPEED INFO FOR EACH ROUTE ON SPECIFIC DAYS BY TAKING SIMPLE AVERAGES
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
printed = []
limit = 90
absurd = 0

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
            spd_dty = entry[j+6].split(',')
            spd_dty = [spd_dty[0][1:],spd_dty[1][:-1]]
            print spd_dty

            speed = float(spd_dty[0])
            density = float(spd_dty[1])
            # look for absurd speeds
            if speed >= limit and route not in printed:
                absurd+=1
                print "SPEED: ",speed
                print "DISTANCE: ",dst
                print
                printed.append(route)

            #check route has been seen
            if route not in routes:
                routes[route] = {day: {}}
                routes[route][day][time] = {}
                routes[route][day][time]["speed"] = speed
                routes[route][day][time]["density"] = density
                routes[route][day]["count"] = 1.0
            # check if day has been seen for route
            elif day not in routes[route]:
                routes[route][day] = {"count": 1.0, time: {"speed": speed, "density": density}}
            # check if time has been seen on this day of week for this route
            elif time not in routes[route][day]:
                routes[route][day][time] = {}
                routes[route][day][time]["speed"] = speed
                routes[route][day][time]["density"] = density
            else:
                routes[route][day][time]["speed"]+= speed
                routes[route][day][time]["density"]+= density
            i=j
            j+=1

        routes[route][day]["count"]+= 1.0

# CALCULATE AVERAGES PER DAY
for route in routes:
    for day in routes[route]:
        for time in routes[route][day]:
            c = routes[route][day]["count"]
            if time!="count":
                routes[route][day][time]["speed"] /= c
                routes[route][day][time]["density"] /= c
                speed = routes[route][day][time]["speed"]
                # look for absurd speeds
                if speed >= limit:
                    absurd+=1
                    print "SPEED: ",speed
                    print "DISTANCE: ",dst
                    print

print "THERE ARE %d ENTRIES WITH SPEEDS OVER %.fmph"%(absurd,limit)

with open(out_file, 'w') as out_f:
        json.dump(routes, out_f, indent=4)
