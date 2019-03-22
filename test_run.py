from env import TELEGRAM_BOT_API_KEY
from env import MY_ID
import parse_modified_data as p_modified_d
import parse_natural_language as parse_nl
from datetime import datetime
import parse_dates as p_dates
import telepot

# print(pda.convertDateToDay(datetime.today()))
# print(p_data.parseSessionData(0, "wednesday"))

bot = telepot.Bot(TELEGRAM_BOT_API_KEY)
output = parse_nl.checkFutureDateNL("25 Apr 2019")

sendstring = ""
for x in output:
	sendstring += x + "\n"
bot.sendMessage(MY_ID, sendstring, parse_mode="Markdown")

# print(parse_nl.checkFutureDate("25 Apr 2019"))

# print(len(p_modified_d.getAppendedSessions("thursday")))
# print(p_cancledd_d.getCancelledSessions("wednesday"))