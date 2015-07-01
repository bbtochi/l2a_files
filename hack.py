import csv
import numpy as np

data_file = 'films.csv'
data = []
with open(data_file, 'r') as data_f:

    # Parse it as a CSV file.
    data_csv = csv.reader(data_f, delimiter=',', quotechar='"')
    
    # Skip the header row.
    next(data_csv, None)

    # Load the data.
    for row in data_csv:
		data.append({ 'title':   row[0],
                         'year': row[1],
                         'location': row[2],      
                         'facts': row[3],
                         'producer': row[4],
                         'distributor': row[5],
                         'director': row[6],
                         'writer': row[7],
                         'actor1': row[8],
                         'actor2': row[9],
                         'actor3': row[10],
                         })        


movies = []
years = {}
x = []
TOTAL = 0
P = []
producer = 0

# THIS IS TO FIND NUMBER OF SF MOVIES PER YEAR
table = []
# go through all the movies
for movie in range(len(data)):
	mv = data[movie]["title"]
	if data[movie]["title"] not in movies:
		movies.append(mv)
		yr = data[movie]["year"]
		if yr in years:
			years[yr]+=1
			TOTAL += 1
		else:
			years[yr] = 1
			x.append(int(yr))
			TOTAL += 1

	if data[movie]["location"] not in P:
		producer+=1
		P.append(data[movie]["location"])

print producer 

# y = [0 for i in range(len(x))]
# # fill up frequency array
# for yr in years:
# 	i = x.index(int(yr))
# 	y[i] = years[yr]


# plt.plot(x,y, 'ro')
# plt.show()

# print TOTAL 
# print years





