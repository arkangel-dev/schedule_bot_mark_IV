import parse_dates as pda
import parse_data as pd
import parse_modified_data as p_modified_d
from datetime import datetime


def getFullTodayNL():
	output_list = []
	bring_laptop = False
	todayDay = pda.convertDateToDay(datetime.today())
	cancelled_session_list = p_modified_d.getCancelledSessions(todayDay)
	appended_session_list = p_modified_d.getAppendedSessions(todayDay)
	session_count = pd.getSessionCount(todayDay) # - len(cancelled_session_list)
	if session_count != 0:
		output_list.append("You have " + str((session_count - len(cancelled_session_list)) + len(appended_session_list)) + " session(s) today. They are the following : \n")
		for x in range(0, session_count):
			dayData = pd.parseSessionData(x, todayDay)
			if str(x) in cancelled_session_list:
				output_list.append("* >  Your " + dayData[0] + " session have been cancelled. *")
			else:
				if dayData[3]:
					bring_laptop = True
				output_list.append("* >  " + dayData[0] + " from " + dayData[1] + " hours to " + dayData[2] + " hours with " + dayData[4] + ". Class will be held at " + str(dayData[5]) + ".*")
		if len(appended_session_list) != 0:
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

	
