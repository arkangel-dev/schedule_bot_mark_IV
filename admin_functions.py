import sys
import json
import telepot
from env import TELEGRAM_BOT_API_KEY
from datetime import datetime
import traceback
import admin_func_lib as admin_func

# ["SESSION_NAME", "STARTING_TIME", "ENDING_TIME", "BRING_LAPTOP_BOOLEAN", "LECTURER_NAME", "VENUE"]

#=========================================================================
# import telepot
# from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

# keyboard = InlineKeyboardMarkup(inline_keyboard=[
#                    [InlineKeyboardButton(text="hey", callback_data='/command1')],
#                    [InlineKeyboardButton(text="hey", callback_data='/command1')],
#                    [InlineKeyboardButton(text="hey", callback_data='/command1')]
#                ])

# bot = telepot.Bot("641334893:AAF1_MJ2ou9nGt4MIbAYSIWMUxfKPDCpDAw")
# bot.sendMessage(488976797, "Hello", reply_markup = keyboard)
#============================================================================

raw = sys.argv[1]
converted = json.loads(raw)
chat_id = converted["chatId"]
content = converted["content"]

if (converted["type"] == "callback_query"):
    queryMode = True
    query_id = converted["callbackQueryId"]
else:
    queryMode = False
    query_id = 0

if len(content.split()):
    command = content.split()[0]
else:
    command = "EnterInteractiveMode"

bot = telepot.Bot(TELEGRAM_BOT_API_KEY)
af_version = 0.5

print("Command : " + command) # debug the command in the node-red command lines...
 
f = open("test_json.json" , "r") # open the append-session file...
file_json = f.read()
append_raw_data = json.loads(file_json)

f = open("session_list.json" , "r") # open the main session file...
file_json = f.read()
session_raw_data = json.loads(file_json)

# check commands...
if (command == "append"): # append_sessions...
    admin_func.append_session(chat_id, content)

elif (command == "cancel_session"):
    x = None

elif (command == "list"):
    admin_func.list_sess(chat_id)

elif (command == "EnterInteractiveMode"): # this is the function that activates the command keybaord...
    admin_func.SendCommandKeyboard(chat_id, "\n *Interactive Mode Enabled* : \n Welcome, please choose a command : ")

elif (command == "raw_list"):
    admin_func.raw_list(chat_id)

elif (command == "help"):
    admin_func.help_list(chat_id, queryMode, query_id)

elif (command == "disableInteractive"):
    bot.sendMessage(chat_id, "Okay, Have a good day.")
    bot.answerCallbackQuery(query_id, "OK, Have a good day.")
    
else: # fall back clause...
    bot.sendMessage(chat_id, "Command not found. Send `/admin help` for a list of commands", parse_mode="markdown")