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
import normie_functions as normie
 
bot = telepot.Bot(TELEGRAM_BOT_API_KEY)

raw = sys.argv[1]
converted = json.loads(raw)
#
# convert the essential information about
# the request so that it can be used to utilize the
# check functions.
#
chatId = converted["chatId"]
content = converted["content"]
command = content.split()[0]
#
# send the request to telegram to send
# the 'typing...' status to the 
# user. This will make delays in send the
# responses more natural
#
bot.sendChatAction(chatId, "typing")
#
# open the nessesary files. the user_status_data.json will
# store whether the bot is expecting the user to enter parameter
# to the bot. It will also store other stuff in future updates.
#
user_status_data = core.openJsonFile("user_status_data.json")
awaiting_response_list = user_status_data["awaiting_response_users"]

#
# check if the request is a callback query. aka check if the request
# originated from a telegram keyboard. if it is from a keyboard exit
# because all keyboard request are handled by the keyboard_stuff.py
# file
#
if (converted["type"] == "callback_query"):
    exit()
# else:
#     # aaaand the fallback
#     # cool? cool cool cool cool
#     queryMode = False
#     query_id = 0
#
# the above fallback was when the node-red server was configued to
# accept keyboard request from only admin function keyboards. Now 
# it is not required, but I'll be leaving it just in case.

if (command == "/cancel"):
	# this cancel function is here because if
	# this file will not be invoked at all
	bot.sendMessage(chatId, "No active command to cancel. I wasn't doing anything anyway. Zzzzz...", parse_mode="markdown")
	exit()

elif (command == "/admin"):
	# exit because this is an admin function and
	# this file has no busness meddling with admin functions...
	#
	# I'll be leaving this if check here just in case if this
	# file gets a request to access the admin keyboard ( which is
	# highly unlikely )
	#
	exit()

if (command == "/today"):
	# send the status data
	# for today's data...
	#
	# this check is used to send the session
	# details for the current day of the week.
	#
	# note how there is for loop doohicky is there.
	# that is because originally thre getFullTodayNL()
	# function was coded so that the function will send the
	# details as a list. How ever this caused some... 'aesthetic'
	# problems.
	#
	sendstring = ""
	output = parse_nl.getFullTodayNL(chatId)
	for x in output:
		sendstring += x + "\n"
	bot.sendMessage(chatId, sendstring, parse_mode="Markdown")
	print("[+] Send Today Data...") 

elif (command == "/start"):
	# send a the response for the 
	# start commands
	# this is the messange that will be sent to the bot. And will be triggered
	# by the "/start" command, which is sent by telegram by default
	#
	bot.sendMessage(chatId, "*Student Mode : * \nUse this to get dates and junk. Basic use : /today . Made for normies", parse_mode="markdown")
	bot.sendMessage(chatId, "*Administrative Mode : * \nThis mode is only accessible by users with special access. If you are registered as an admin send /admin to start interactive mode.", parse_mode="markdown")

elif (command == "/register"):
	# send a keyboard so the user can register
	# their account to a programme, an intake and an year
	#
	normie.registerUser(chatId, content)

else:
	# this is the fallback
	# condition. incase the command does not match
	# any functions programmed in
	bot.sendMessage(chatId, "I'm sorry, what?")