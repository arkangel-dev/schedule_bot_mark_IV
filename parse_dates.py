# parse dates
from datetime import datetime
import parse_data

def convertDateToDay(raw_date):
	# raw_date = datetime.today()
	dayNo = raw_date.weekday()
	daysArray = ("monday","tuesday","wednesday","thursday","friday","saturday","sunday")
	dayName = daysArray[dayNo]
	return(dayName)
		
def convertStringToDatetime(raw_string):
	try:
		datetime_object = datetime.strptime(raw_string, '%d %b %Y')
		return(datetime_object)
	except ValueError: 
		return("InvalidFormat")