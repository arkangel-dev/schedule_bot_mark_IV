import parse_dates as pda
import parse_data as pd
import parse_cancelled_data as p_cancledd_d
from datetime import datetime


def getFullTodayNL():
	output_list = []
	bring_laptop = False
	todayDay = pda.convertDateToDay(datetime.today())
	cancelled_session_list = p_cancledd_d.getCancelledSessions(todayDay)
	session_count = pd.getSessionCount(todayDay) # - len(cancelled_session_list)
	if session_count != 0:
		output_list.append("You have " + str(session_count) + " session(s) today. They are the following : ")
		for x in range(0, session_count):
			dayData = pd.parseSessionData(x, todayDay)
			if str(x) in cancelled_session_list:
				output_list.append("Your " + dayData[0] + " session have been cancelled")
			else:
				if dayData[6]:
					bring_laptop = True
				output_list.append("You have " + dayData[0] + " from " + dayData[1] + " hours to " + dayData[2] + " hours with " + dayData[4] + ". Class will be held at " + str(dayData[5]) + ".")
		if bring_laptop:
			output_list.append("You'll also need to bring your laptop. Dont forget to charge it")
		else:
			output_list.append("You won't be needing your laptop")
	else:
		output_list.append("You don't have any sessions today.")
	return(output_list)
	
