"""
* READ IN DATA WITH CORRECT DISTANCES
* CHANGE DISTANCES TO MILES
* CALCULATE ESTIMATED SPEEDS FOR EACH TIME BLOCK
* WRITE DATA WITH ESTIMATED SPEED INFORMATION TO OUTPUT FILE
"""
import csv
import json

in_file = "output.csv"
out_file = "speed_estimates"
data = []
times = []
routes = []
c = 0
large = 0


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
# returns the estimated speed at any given minute for some roadway
def speed_est(length, flowrate):
    global c,prev_length
    fr = float(flowrate)
    # number of vehicle that must cross distance per minute to get desired flowrate
    vhs_per_min = fr/60.

    # time (in hours) it would take one car to cover distance
    time = (1.0/vhs_per_min)/60.0
    speed = truedist(length)/time
    # print "TIME: %.fmins"%(time*60.0)
    # l = length.split(" ")
    # if len(l)>1:
    #     if time < 1./6.:
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
    return speed

with open(in_file, 'r') as in_f:
    # parse as csv file
    in_csv = csv.reader(in_f, delimiter=',', quotechar='"')

    next(in_csv, None)

    # go through each entry and estimate speed
    for entry in in_csv:
        dic = {'id': entry[1], 'origin': entry[2], 'destination': entry[3], 'direction': entry[4], 'distance': entry[5], 'date': entry[6], 'day': entry[7] }

        print "HERE!!"

        # fix distance unit error
        if len(dic['distance'].split(" ")) == 1:
            dic["distance"] = dic["distance"][:-1]+" m"

        # look for entries with large distances
        r = (entry[2],entry[3])
        if r not in routes:
            routes.append(r)
            ds = dic['distance'].split(" ")
            d = float(ds[0])
            if d > 3.0 and ds[1] == "km":
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

            # make speed estimate
            dic[key] = speed_est(dic['distance'],fr)
            i=j
            j+=1
        data.append(dic)

print "COUNT:",c

# WRITE DATA WITH SPEED ESTIMATES TO OUTPUT FILE
with open(out_file, 'w') as out_f:
    # Produce a CSV file.
    out_csv = csv.writer(out_f, delimiter=',', quotechar='"', lineterminator='\n')

    # Write the header row.
    out_csv.writerow(['ID','ORIGIN','DESTINATION','DIR','DISTANCE','DATE','DAY']+times)

    for entry in data:
        # get estimated speed info for each entry
        spds = []
        for time in times:
            spds.append(entry[time])

        # write row to file
        row = [entry["id"],entry["origin"],entry["destination"],entry["direction"],entry["distance"],entry["date"],entry["day"]]+spds
        out_csv.writerow(row)

print "THERE ARE STILL %d ENTRIES WITH DISTANCE > 3 KM FROM INPUT DATA"%large

"""
Still wrong:
81.2
16.4
16.3
258
17.3 km
261 km
8.9 km

Apparently correct:
12 km
3 km
30.9 km
4.67 km
38.8 km
44.4 km
19.3 km
"""
