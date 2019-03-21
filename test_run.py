import parse_modified_data as p_modified_d
import parse_natural_language as parse_nl
from datetime import datetime
import telepot

# print(pda.convertDateToDay(datetime.today()))
# print(p_data.parseSessionData(0, "wednesday"))


bot = telepot.Bot("641334893:AAF1_MJ2ou9nGt4MIbAYSIWMUxfKPDCpDAw")
output = parse_nl.getFullTodayNL()
for x in output:
	bot.sendMessage(488976797, x)

# print(len(p_modified_d.getAppendedSessions("thursday")))
# print(p_cancledd_d.getCancelledSessions("wednesday"))

