import parse_dates as pda
import parse_data as pd
from datetime import datetime


def getFullTodayNL():
	output_list = []
	bring_laptop = False
	todayDay = pda.convertDateToDay(datetime.today())
	session_count = pd.getSessionCount(todayDay)
	output_list.append("You have " + str(session_count) + " session(s) today. They are the following : ")
	
	for x in range(0, session_count):
		dayData = pd.parseSessionData(x, todayDay)
		if dayData[6]:
			bring_laptop = True
		output_list.append("You have " + dayData[0] + " from " + dayData[1] + " hours to " + dayData[2] + " hours with " + dayData[4] + ". Class will be held at " + str(dayData[5]) + ".")
	
	if bring_laptop:
		output_list.append("You'll also need to bring your laptop. Dont forget to charge it")
	else:
		output_list.append("You won't be needing your laptop")

	# Convert to string without messing with Isaam's code.
	final_text = ''
	for text in output_list:
		final_text += text
		
	return(final_text)
