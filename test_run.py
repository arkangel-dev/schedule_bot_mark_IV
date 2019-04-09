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

user_status_data = core.openJsonFile("user_status_data.json")
awaiting_response_list = user_status_data["awaiting_response_users"]

if (command == "/cancel"):
	exit()

if (command == "/today"):
	sendstring = ""
	output = parse_nl.getFullTodayNL()
	for x in output:
		sendstring += x + "\n"
	bot.sendMessage(chatId, sendstring, parse_mode="Markdown")
	print("[+] Send Today Data...")

if (command == "/start"):
	bot.sendMessage(chatId, "*Start Administrative Mode : * \nInteractive mode disabled. You now have to use command lines. Send /admin to start interactive mode. Send `/admin help` to get a list of commands.", parse_mode="markdown")
