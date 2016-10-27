
import requests
import pyrebase # becuase of this needs to be run with Python 2 (not 3) on Windows
from datetime import datetime
from os import path

URL = 'https://my.engr.illinois.edu/labtrack/util_data_json.asp'
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

def get_json(_URL):
    num_tries, max_tries = (0, 5)
    status_code = -1
    while(status_code != 200 and num_tries < max_tries):
        response = requests.get(_URL)
        status_code = response.status_code
        num_tries += 1
    if (status_code != 200):
        return False
    return response.json()

def save_workstation_usage():
    workstationsData = get_json(URL)
    if (workstationsData == False):
        print('Error: get_json returned False, not adding any new logs')
        return

    workstations = workstationsData["data"]
    workstationValues = {}
    for workstation in workstations:
        logging_datetime = datetime.utcnow().strftime("%m-%d-%y %H:%M:%S")
        computersUsed = str(workstation["inusecount"]) + "/" + str(workstation["machinecount"])
        workstationValues[workstation["strlabname"]] = (logging_datetime, computersUsed)

    for lab in workstationValues:
        logging_datetime, computersUsed = workstationValues[lab]
        db.child("ews-workstations").child(lab).child(logging_datetime).set(computersUsed)
        
    print('Finished saving workstation usage (' + logging_datetime + ')')

firebase = init_firebase()
db = firebase.database()
save_workstation_usage()
