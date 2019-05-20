import parse_dates as pda
import parse_data as pd
import parse_modified_data as p_modified_d
from datetime import datetime


def getFullTodayNL(chat_id):
	output_list = []
	bring_laptop = False
	todayDay = pda.convertDateToDay(datetime.today())
	cancelled_session_list = p_modified_d.getCancelledSessions(todayDay)
	cancelled_session_list_count = len(cancelled_session_list)

	appended_session_list = p_modified_d.getAppendedSessions(todayDay) # open up the json file
	
	if (appended_session_list == None):
		appended_session_list_count = 0
	else:
		appended_session_list_count = len(appended_session_list)

	session_count = pd.getSessionCount(todayDay, chat_id) # - len(cancelled_session_list) # tampering with this variable for the double for loops will cause issues
	if session_count != 0: # check if there are any sessions...
		output_list.append("You have " + str((session_count - cancelled_session_list_count) + appended_session_list_count) + " session(s) today. They are the following : \n")
		for x in range(0, session_count):
			dayData = pd.parseSessionData(chat_id, x, todayDay)
			if str(x) in cancelled_session_list: # check if the session was cancelled via the modified json file..
				output_list.append("* >  Your " + dayData[0] + " session have been cancelled.*") # if cancelled add this line to the append...
			else:
				if dayData[3]: # check if you have to bring your laptop...
					bring_laptop = True # set the boolean to True
				output_list.append("* >  " + dayData[0] + " from " + dayData[1] + " hours to " + dayData[2] + " hours with " + dayData[4] + ". Class will be held at " + str(dayData[5]) + ".*")
		if appended_session_list_count != 0: # check if there are any appended sessions...
			output_list.append("\nIn addition to your regular classes you also have the following appended class(es) : \n")
			for x in range(0, len(appended_session_list)):
				output_list.append("* >  " + appended_session_list[x][0] + " from " + appended_session_list[x][1] + " hours to " + appended_session_list[x][2] + " hours with " + appended_session_list[x][4] + ", at " + appended_session_list[x][5] + ".*")
				if pd.parseBooleans(appended_session_list[x][3]):
					bring_laptop = True
		if bring_laptop:
			output_list.append("\nYou'll also need to bring your laptop. Dont forget to charge it")
		else:
			output_list.append("\nYou won't be needing your laptop")
	else:
		output_list.append("You don't have any sessions today.")
	return(output_list)

# def checkFutureDateNL(raw_string):
# 	# This function will be used to check if there any sessions of a future date...
# 	output_list = []
# 	raw_date = pda.convertStringToDatetime(raw_string)
# 	date_weekday = pda.convertDateToDay(raw_date)
# 	raw_data = pd.parseSessionData
# 	session_count = pd.getSessionCount(date_weekday)

# 	if (session_count != 0):
# 		output_list.append("You have " + str(session_count) + " sessions that day. They are the following : \n")
# 		for x in range(0, session_count):
# 			dayData = raw_data(x, date_weekday)
# 			output_list.append("* >   " + dayData[0] + " from " + dayData[1] + " hours to " + dayData[2] + " hours with " + dayData[4] + ". Class will be held at " + str(dayData[5]) + ".*")
# 	else:
# 		output_list.append("You dont have any sessions on that day.")
# 	return(output_list)
