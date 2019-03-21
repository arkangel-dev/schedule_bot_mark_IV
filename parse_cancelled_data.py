# Parse cancelled data...
import json

with open('cancelled_sessions_list.json') as f:
	cancelled_data_raw = json.load(f)
	
def getCancelledSessions(day):
	cancelled_sessions = cancelled_data_raw["cancelled"][day]
	return(cancelled_sessions)