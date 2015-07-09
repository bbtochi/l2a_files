"""
* READ IN DATA WITH CORRECT DISTANCES
* CHANGE DISTANCDS TO MILES
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
        #print "WRONG"
        return val*0.621371

# returns the estimated speed at any given minutet for some roadway
def speed_est(length, flowrate):
    fr = float(flowrate)
    vhs_per_min = fr/60.
    # print "VEHICLES/min: %f"%fr

    # time (in hours) it would take one car to cover distance
    time = (1.0/vhs_per_min)
    # print "TIME: %.fmins"%(time*60.0)
    return time

with open(in_file, 'r') as in_f:
    # parse as csv file
    in_csv = csv.reader(in_f, delimiter=',', quotechar='"')

    next(in_csv, None)

    # go through each entry and estimate speed
    entry_count = 0
    for entry in in_csv:
        dic = {'id': entry[1], 'origin': entry[2], 'destination': entry[3], 'direction': entry[4], 'distance': entry[5], 'date': entry[6], 'day': entry[7] }

        # add in speed estimates
        i = 24
        j = 1
        while j != 25:
            key = str(i)+':00-'+str(j)+':00'
            if key not in times:
                times.append(key)
            # handle 0 counts for flowrate
            fr = entry[j+7]
            if fr == '0':
                fr = '1'
            dic[key] = speed_est(dic['distance'],fr)
            # print "WE HAVE AN ESTIMATE: %f"%dic[key]
            # print "FLOWRATE: "+entry[j+7]+"vhs/hr"
            # print "DISTANCE: "+dic["distance"]
            # print
            i=j
            j+=1
        entry_count+=1
        data.append(dic)

with open(out_file, 'w') as out_f:
    # Produce a CSV file.
    out_csv = csv.writer(out_f, delimiter=',', quotechar='"', lineterminator='\n')

    # Write the header row.
    out_csv.writerow(['ID','ORIGIN','DESTINATION','DIR','DISTANCE','DATE','DAY']+times)

    for entry in data:
        # get flow rates info for each entry
        spds = []
        for time in times:
            spds.append(entry[time])

        # write row to file
        row = [entry["id"],entry["origin"],entry["destination"],entry["direction"],entry["distance"],entry["date"],entry["day"]]+spds
        out_csv.writerow(row)
        # json.dump(entry, out_f, indent=8)

print "input: ",entry_count
print "output: ",len(data)
