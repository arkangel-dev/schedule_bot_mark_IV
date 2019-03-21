# parse dates
from datetime import datetime
import parse_data

def convertDateToDay(raw_date):
		dayNo = raw_date.weekday()
		daysArray = ("monday","tuesday","wednesday","thursday","friday","saturday","sunday")
		dayName = daysArray[dayNo]
		return(dayName)
		