import parse_modified_data as p_modified_d
import parse_natural_language as parse_nl
from datetime import datetime
import telepot

# print(pda.convertDateToDay(datetime.today()))
# print(p_data.parseSessionData(0, "wednesday"))

# DONT YOU FUCKING DARE SPAM WITH THIS BOT!!!
bot = telepot.Bot("641334893:AAF1_MJ2ou9nGt4MIbAYSIWMUxfKPDCpDAw")
output = parse_nl.getFullTodayNL()
sendstring = ""
for x in output:
	sendstring += x + "\n"
bot.sendMessage(488976797, sendstring, parse_mode="Markdown")


# print(len(p_modified_d.getAppendedSessions("thursday")))
# print(p_cancledd_d.getCancelledSessions("wednesday"))

