
# when run, this script will pull most recent data for the ews_workstations
# and create a new and updated graph

import pyrebase
import numpy as np
import json
import matplotlib.pyplot as plt
from os import path
from datetime import datetime

file_loc = path.dirname(path.realpath(__file__))

def init_firebase():
	config = {
  	  	"apiKey": "", # should be in serviceAccount file, which is at root of project
  		"authDomain": "datalok-f7bab.firebaseapp.com",
  		"databaseURL": "https://datalok-f7bab.firebaseio.com",
  		"storageBucket": "datalok-f7bab.appspot.com",
  		"serviceAccount": file_loc + "/../../datalok.json" 
	} 
	return pyrebase.initialize_app(config)

def save_obj(obj, name):
    with open('data/'+ name + '.json', 'w') as f:
        json.dump(obj, f)

# convert a utc time to cdt
def utc_to_cdt(utc_time):
	return (int(utc_time) - 5) % 24

# init firebase
firebase = init_firebase()
db = firebase.database()

# get the workstations (this is a dict)
workstations = db.child("ews-workstations").get().val()

# helper dict stores the max number of computers at each workstation
max_comps_dict = {}

# create dict, for each hour of each workstation, a list of usage numbers
usage = {}
for workstation in workstations:
	usage[workstation] = {}
	for log in workstations[workstation]:
		hour = utc_to_cdt(datetime.strptime(log, "%m-%d-%y %H:%M:%S").hour)
		amt_in_use = workstations[workstation][log].split('/')[0]
		max_comps = workstations[workstation][log].split('/')[1]
		if hour not in usage[workstation].keys():
			usage[workstation][hour] = []
		usage[workstation][hour].append(amt_in_use)
		if workstation not in max_comps_dict:
			max_comps_dict[workstation] = max_comps

# create another dict, this one with an avg for each hour value
usage_stats = {}
for workstation in usage:
	usage_stats[workstation] = {}
	for i in range(24):
		avg = np.average(np.array(usage[workstation][i]).astype(np.float))
		avg = round(avg, 2)
		num_samples = len(usage[workstation][i])
		max_computers = max_comps_dict[workstation]
		usage_stats[workstation][i] = {}
		usage_stats[workstation][i]['avg'] = avg
		usage_stats[workstation][i]['num_samples'] = num_samples
		usage_stats[workstation][i]['max_computers'] = max_computers

# have data on everything we need, now put into graph format
for workstation in usage_stats:
	plt.figure()
	plt.xlabel("Hours (CDT)")
	plt.ylabel("Computers In Use")
	plt.title(workstation)
	x = [i for i in usage_stats[workstation]]
	y = [usage_stats[workstation][j]['avg'] for j in usage_stats[workstation]]
	plt.plot(x, y)
	plt.savefig('graphs/' + workstation + '.png')