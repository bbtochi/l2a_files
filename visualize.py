"""
PRODUCES VISUALIZATIONS OF OUR DATA
"""
import matplotlib
from matplotlib import pyplot as pp
from matplotlib import rcParams
import csv

# removes leading and trailing spaces in a string
def clean_row(row,i):
    while row[i][0] == " " or row[i][-1] == " ":
        if row[i][0] == " ":
            row[i] = row[i][1:]
        elif row[i][-1] == " ":
            row[i] = row[i][:-1]

# given metric distance as string, returns distance in miles
def truedist(d):
    dst = d.split(" ")
    val, unit = float(dst[0]), dst[1]
    # convert to miles
    if unit == 'm':
        return val*0.000621371
    else:
        return val*0.621371

# returns the estimated speed and density at any given minute for some roadway
def density_est(length, flowrate):
    global c,prev_length
    fr = float(flowrate)
    # number of vehicle that must cross distance per minute to get desired flowrate
    vhs_per_min = fr/60.

    # time (in hours) it would take one car to cover distance
    distance = truedist(length)
    density = vhs_per_min/distance

    return density

# ope ny data file
with open('nytraffic.csv', 'rU') as in_f:
    in_csv = csv.reader(in_f, delimiter=',', quotechar='"')

    # skip header
    next(in_csv,None)

    # get first route
    for row in in_csv:
        print row

        clean_row(row,2)
        clean_row(row,3)
        clean_row(row,4)

        # assign origin and destination information
        o = row[2]+" and "+row[3]+", NY"
        d = row[2]+" and "+row[4]+", NY"
        title = "Route Traffic Flowrate Between "+o+" AND "+d

        # get count info
        left, lefts, heights, labels, colors = 0, [], [], [], []
        for i in range(24):
            lefts.append(left)
            heights.append(density_est('80 m', row[i+7]))
            labels.append(str(i)+':00')
            colors.append('r')
            left+=.5
        break

    f = pp.figure()
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 8}

    matplotlib.rc('font', **font)
    ax = f.add_axes([0.05,0.05,0.9,.9], xlabel='time of day', ylabel='vehicles/hour', title=title)
    ax.bar(lefts,heights,width=.5,color=colors)
    ax.set_xticks(lefts)
    ax.set_xticklabels(labels)
    pp.show()
