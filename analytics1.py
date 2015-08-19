"""
* READ IN DATA WITH CORRECT DISTANCES
* CHANGE DISTANCES TO MILES
* CALCULATE ESTIMATED SPEEDS FOR EACH TIME BLOCK
* WRITE DATA WITH ESTIMATED SPEED INFORMATION TO OUTPUT FILE
"""
import csv
import json

in_file = "right_distances.csv"
out_file = "speed_estimates"
data = []
times = []
routes = []
c = 0
large = 0
limit = 80.0


# given metric distance as string, returns distance in miles
def truedist(d):
    dst = d.split(" ")
    val, unit = float(dst[0]), dst[1]
    # convert to miles
    if unit == 'm':
        return val*0.000621371
    else:
        return val*0.621371

prev_length = "none"
# returns the estimated speed and density at any given minute for some roadway
def speed_est(length, flowrate):
    global c,prev_length
    fr = float(flowrate)
    # number of vehicle that must cross distance per minute to get desired flowrate
    vhs_per_min = fr/60.

    # time (in hours) it would take one car to cover distance
    distance = truedist(length)
    time = (1.0/vhs_per_min)/60.0
    speed = distance/time
    density = vhs_per_min/distance

    # correct crazy speeds,considering distance to be covered
    if speed > limit:
        if distance < 3.0:
            speed = 55.0
        else:
            speed = 65.0

    # detect distances that give crazy speeds
    # print "TIME: %.fmins"%(time*60.0)
    # l = length.split(" ")
    # if len(l)>1:
    #     if time < 4./60.:
    #         #print "TIME:", time, "min"
    #         if float(l[0])>=.04 and l[1] == "km":
    #             if prev_length == "none":
    #                 c+=1
    #                 print "DISTANCE:", length
    #                 print "TIME:", time, "min"
    #                 print
    #             elif length != prev_length:
    #                 c+=1
    #                 print "DISTANCE:", length
    #                 print "TIME:", time, "min"
    #                 print
    #             prev_length = length
    return (speed,density)

# READ IN DATA WITH CORRECT DISTANCES
with open(in_file, 'r') as in_f:
    # parse as csv file
    in_csv = csv.reader(in_f, delimiter=';', quotechar='"')

    next(in_csv, None)

    # go through each entry and estimate speed
    for entry in in_csv:
        dic = {'id': entry[1], 'origin': entry[2], 'destination': entry[3], 'direction': entry[4], 'distance': entry[5], 'date': entry[6], 'day': entry[7] }

        # fix distance unit error
        if len(dic['distance'].split(" ")) == 1:
            dic["distance"] = dic["distance"][:-1]+" m"

        # look for entries with large distances
        r = (entry[2],entry[3])
        if r not in routes:
            routes.append(r)
            ds = dic['distance'].split(" ")
            d = float(ds[0])
            if d > 3.0 and ds[1] == "km" or d < 4.0 and ds[1] == "m":
                # print dic["distance"]
                large+=1

        # add in speed estimates
        i,j = 24,1
        while j != 25:
            key = str(i)+':00-'+str(j)+':00'
            if key not in times:
                times.append(key)

            # handle 0 counts for flowrate
            fr = entry[j+7]
            if fr == '0':
                fr = '2'

            # make speed and density estimate
            dic[key] = speed_est(dic['distance'],fr)
            i=j
            j+=1

        data.append(dic)

print "COUNT:",c

# WRITE DATA WITH SPEED ESTIMATES TO OUTPUT FILE
with open(out_file, 'w') as out_f:
    # Produce a CSV file.
    out_csv = csv.writer(out_f, delimiter=';', quotechar='"', lineterminator='\n')

    # Write the header row.
    out_csv.writerow(['ID','ORIGIN','DESTINATION','DIR','DISTANCE','DATE','DAY']+times)

    for entry in data:
        # get estimated (speed,density) info for each entry
        spds = []
        for time in times:
            spds.append(entry[time])

        # write row to file
        row = [entry["id"],entry["origin"],entry["destination"],entry["direction"],entry["distance"],entry["date"],entry["day"]]+spds
        out_csv.writerow(row)

print "THERE ARE STILL %d ENTRIES WITH DISTANCE > 3 KM OR < 4 M FROM INPUT DATA"%large
