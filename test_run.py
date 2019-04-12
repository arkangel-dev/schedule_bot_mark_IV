from env import TELEGRAM_BOT_API_KEY
from env import MY_ID
import parse_modified_data as p_modified_d
import parse_natural_language as parse_nl
from datetime import datetime
import parse_dates as p_dates
import telepot
import sys
import json
import core_functions as core
 
bot = telepot.Bot(TELEGRAM_BOT_API_KEY)

raw = sys.argv[1]
converted = json.loads(raw)
chatId = converted["chatId"]
content = converted["content"]
command = content.split()[0]
bot.sendChatAction(chatId, "typing")
user_status_data = core.openJsonFile("user_status_data.json")
awaiting_response_list = user_status_data["awaiting_response_users"]

if (command == "/cancel"):
	# this cancel function is here because if
	# this file will not be invoked at all
	bot.sendMessage(chatId, "No active command to cancel. I wasn't doing anything anyway. Zzzzz...", parse_mode="markdown")
	exit()

elif (command == "/admin"):
	# exit because this is an admin function and
	# this file has no busness meddling with admin functions...
	exit()

if (command == "/today"):
	# send the status data
	# for today's data...
	sendstring = ""
	output = parse_nl.getFullTodayNL()
	for x in output:
		sendstring += x + "\n"
	bot.sendMessage(chatId, sendstring, parse_mode="Markdown")
	print("[+] Send Today Data...") 

elif (command == "/start"):
	# send a the response for the 
	# start commands
	bot.sendMessage(chatId, "*Normie Mode : * \nUse this to get dates and junk. For normies", parse_mode="markdown")
	bot.sendMessage(chatId, "*🔥 Administrative Mode 🔥 : * \nThis mode is only accessible by users with special access. If you are registered as an admin send /admin to start interactive mode.", parse_mode="markdown")

else:
	# this is the fallback
	# condition. incase the command does not match
	# any functions programmed in
	bot.sendMessage(chatId, "I'm sorry, what?")