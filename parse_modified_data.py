# Parse cancelled data...
import json

with open('appended_sessions_list.json') as f:
	modified_data_raw = json.load(f)
	
def getCancelledSessions(day):
	cancelled_sessions = modified_data_raw["cancelled"][day]
	return(cancelled_sessions)

def getAppendedSessions(day):
	appended_sessions = modified_data_raw["appended"][day]
	return(appended_sessions)