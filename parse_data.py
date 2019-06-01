import json
import parse_dates
import core_functions as core
import env
import telepot

# f = open("user_list.json" , "r")
# file_json = f.read()
# raw_data = json.loads(file_json)
raw_data = core.openJsonFile("session_list.json")

# f = open("appended_session_list.json" , "r")
# file_json = f.read()
append_raw_data = core.openJsonFile("appended_sessions_list.json")

# session_count = len(raw_data["days"]["wednesday"]["sessions"])

def getUserSubscription(chat_id):
	#
	# The user subscribtion data returns an array of 3 values, the
	# year of enrollment, the programme the user is studying and the
	# month of intake.
	#
	raw_subscription_file = core.openJsonFile("subscriptions.json")
	if (str(chat_id) in raw_subscription_file["subscriptions"]):
		subscription_data = raw_subscription_file["subscriptions"][str(chat_id)]
		return(subscription_data)
	else:
		bot = telepot.Bot(env.TELEGRAM_BOT_API_KEY)
		#
		# since this function is invoked every time the bot request to get
		# the day details. If the user has not previous data registered this clause
		# will executed and will exit.
		#
		bot.sendMessage(chat_id, "Hmm, It seems that you are not registered. Please send /register to register your account to a programme and an intake.")
		exit()

def getSessionCount(day, chat_id):
	#
	# returns a count of all session
	# of a specified date...
	#
	intake = getUserSubscription(chat_id)[0]
	programme = getUserSubscription(chat_id)[1]
	year = getUserSubscription(chat_id)[2]
	count = len(raw_data[year][programme][intake.lower()][day.lower()]["sessions"])
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
	#
	# convert the string boolean values into
	# actual boolean type data variables...
	# this function just converts stringed booleans to
	# actual booleans
	#
	if raw_string == "True":
		return(True)
	elif raw_string == "False":
		return(False)
	else:
		return(None)