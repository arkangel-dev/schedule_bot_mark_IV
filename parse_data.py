import json
import parse_dates
import core_functions as core

f = open("session_list.json" , "r")
file_json = f.read()
raw_data = json.loads(file_json)

f = open("appended_sessions_list.json" , "r")
file_json = f.read()
append_raw_data = json.loads(file_json)

# session_count = len(raw_data["days"]["wednesday"]["sessions"])

def getUserSubscription(chat_id):
	raw_subscription_file = core.openJsonFile("subscriptions.json")
	subscription_data = raw_subscription_file["subscriptions"][str(chat_id)]
	return(subscription_data)

def getSessionCount(day, chat_id):
	# returns a count of all session
	# of a specified date...
	intake = getUserSubscription(chat_id)[0]
	programme = getUserSubscription(chat_id)[1]
	year = getUserSubscription(chat_id)[2]
	count = len(raw_data[year][programme][intake][day.lower()]["sessions"])
	return(count)

def parseSessionData(chat_id, session_id, day):
	# send detailed information about a specific
	# specified session of a specified day...
	intake = getUserSubscription(chat_id)[0]
	programme = getUserSubscription(chat_id)[1]
	year = getUserSubscription(chat_id)[2]
	if (getSessionCount(day, chat_id) != 0):

		session_name	= raw_data[year][programme][intake][day]["sessions"][session_id][0]
		start_time		= raw_data[year][programme][intake][day]["sessions"][session_id][1]
		end_time		= raw_data[year][programme][intake][day]["sessions"][session_id][2]
		bring_laptop	= parseBooleans(raw_data[year][programme][intake][day]["sessions"][session_id][3])
		lectuer			= raw_data[year][programme][intake][day]["sessions"][session_id][4]
		venue			= raw_data[year][programme][intake][day]["sessions"][session_id][5]
		return(session_name, start_time, end_time, bring_laptop, lectuer, venue)


def getCancelledSessionsByDay(day):
	# get the cancelled session list
	# inputs : DayName
	session_list = append_raw_data["cancelled"][day.lower()]
	return(session_list)


def parseBooleans(raw_string):
	# convert the string boolean values into
	# actual boolean type data variables...
	if raw_string == "True":
		return(True)
	elif raw_string == "False":
		return(False)
	else:
		return(None)