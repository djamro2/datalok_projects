
import requests
import pyrebase # becuase of this needs to be run with Python 2 (not 3) on Windows
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

URL = 'https://my.engr.illinois.edu/labtrack/util_data_json.asp'

def init_firebase():
	config = {
  		"apiKey": "", # should be in serviceAccount file, which is at root of project
  		"authDomain": "datalok-f7bab.firebaseapp.com",
  		"databaseURL": "https://datalok-f7bab.firebaseio.com",
  		"storageBucket": "datalok-f7bab.appspot.com",
  		"serviceAccount": "./../../datalok.json" 
	}
	return pyrebase.initialize_app(config)

def get_json(_URL):
        try: 
            response = requests.get(_URL)
            return response.json()
        except requests.exceptions.RequestException as e:
            print('Error getting URL: ' + e)
            return False

def save_workstation_usage():
        workstationsData = get_json(URL)
        if (workstationsData == False):
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

scheduler = BlockingScheduler()
scheduler.add_job(save_workstation_usage, 'interval', hours=1)
scheduler.start()
