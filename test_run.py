from env import TELEGRAM_BOT_API_KEY
from env import MY_ID
import parse_modified_data as p_modified_d
import parse_natural_language as parse_nl
from datetime import datetime
import parse_dates as p_dates
import telepot
import sys
import json

bot = telepot.Bot(TELEGRAM_BOT_API_KEY)

raw = sys.argv[1]
converted = json.loads(raw)
chatId = converted["chatId"]
content = converted["content"]
command = content.split()[0]

if (command == "/today"):
	sendstring = ""
	output = parse_nl.getFullTodayNL()
	for x in output:
		sendstring += x + "\n"
	bot.sendMessage(MY_ID, sendstring, parse_mode="Markdown")
	print("[+] Send Today Data...")