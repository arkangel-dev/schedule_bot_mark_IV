import json
import parse_dates

# with open('session_list.json') as f:
	# raw_data = json.load(f)

f = open("session_list.json" , "r")
file_json = f.read()
raw_data = json.loads(file_json)

session_count = len(raw_data["days"]["wednesday"]["sessions"])

def getSessionCount(day):
	count = len(raw_data["days"][day]["sessions"])
	return(count)

def parseSessionData(session_id, day):
	session_name	= raw_data["days"][day]["sessions"][session_id][0]
	start_time		= raw_data["days"][day]["sessions"][session_id][1]
	end_time		= raw_data["days"][day]["sessions"][session_id][2]
	bring_laptop	= parseBooleans(raw_data["days"][day]["sessions"][session_id][3])
	lectuer			= raw_data["days"][day]["sessions"][session_id][4]
	venue			= raw_data["days"][day]["sessions"][session_id][5]
	bring_snacks	= parseBooleans(raw_data["days"][day]["sessions"][session_id][6])
	return(session_name, start_time, end_time, bring_laptop, lectuer, venue, bring_snacks)
	

def parseBooleans(raw_string):
	if raw_string == "True":
		return(True)
	elif raw_string == "False":
		return(False)
	else:
		return(None)