import json
import parse_dates

f = open("session_list.json" , "r")
file_json = f.read()
raw_data = json.loads(file_json)
session_count = len(raw_data["days"]["wednesday"]["sessions"])

def getSessionCount(day):
	# returns a count of all session
	# of a specified date...
	count = len(raw_data["days"][day.lower()]["sessions"])
	return(count)

def parseSessionData(session_id, day):
	# send detailed information about a specific
	# specified session of a specified day...
	if (getSessionCount(day) != 0):
		session_name	= raw_data["days"][day]["sessions"][session_id][0]
		start_time		= raw_data["days"][day]["sessions"][session_id][1]
		end_time		= raw_data["days"][day]["sessions"][session_id][2]
		bring_laptop	= parseBooleans(raw_data["days"][day]["sessions"][session_id][3])
		lectuer			= raw_data["days"][day]["sessions"][session_id][4]
		venue			= raw_data["days"][day]["sessions"][session_id][5]
		return(session_name, start_time, end_time, bring_laptop, lectuer, venue)

def parseBooleans(raw_string):
	# convert the string boolean values into
	# actual boolean type data variables...
	if raw_string == "True":
		return(True)
	elif raw_string == "False":
		return(False)
	else:
		return(None)