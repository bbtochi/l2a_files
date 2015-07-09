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

# given metric distance as string, returns distance in miles
def truedist(d):
    dst = d.split(" ")
    val, unit = float(dst[0]), dst[1]
    # convert to miles
    if unit == 'm':
        return val*0.000621371
    else:
        return val*0.621371

c = 0

# returns the estimated speed at any given minute for some roadway
def speed_est(length, flowrate):
    global c

    fr = float(flowrate)
    # number of vehicle that must cross distance per minute to get desired flowrate
    vhs_per_min = fr/60.

    # time (in hours) it would take one car to cover distance
    time = (1.0/vhs_per_min)
    # print "TIME: %.fmins"%(time*60.0)
    l = length.split(" ")
    if len(l)>1:
        if time < 1./6. and length == '1 m':
            c+=1
            print "TIME:", time, "min"
            print "DISTANCE:", length

    return time

with open(in_file, 'r') as in_f:
    # parse as csv file
    in_csv = csv.reader(in_f, delimiter=',', quotechar='"')

    next(in_csv, None)

    # go through each entry and estimate speed
    for entry in in_csv:
        dic = {'id': entry[1], 'origin': entry[2], 'destination': entry[3], 'direction': entry[4], 'distance': entry[5], 'date': entry[6], 'day': entry[7] }

        # add in speed estimates
        i,j = 24,1
        while j != 25:
            key = str(i)+':00-'+str(j)+':00'
            if key not in times:
                times.append(key)

            # handle 0 counts for flowrate
            fr = entry[j+7]
            if fr == '0':
                fr = '1'

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

