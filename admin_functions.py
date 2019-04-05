import sys
import json
import telepot
from env import TELEGRAM_BOT_API_KEY
from datetime import datetime
import traceback
import admin_func_lib as admin_func
import core_functions as core

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
    # if the command is available
    # set the command variable
    command = content.split()[0]
else:
    # or else that means only /admin
    # was pased... Then enter
    # interactive mode
    command = "EnterInteractiveMode"

bot = telepot.Bot(TELEGRAM_BOT_API_KEY)

print("Command : " + command) # debug the command in the node-red command lines...

# check commands...
if (command == "append"):
    # append the sessions to the
    # main sessions list system
    admin_func.append_session(chat_id, content)

elif (command == "cancel_session"):
    # This function is a part of the cancel functions...
    # this command will send a list of all the days
    # from which you can send one to cancel that
    # day's session(s)
    admin_func.Cancel_SendDayList(chat_id)

elif (command == "cancel_getsessionid"):
    # This function is part of the cancel function
    # This command will send a list of all sessions
    # on that day...
    # inputs : DayName
    dayname = content.split()[1]
    admin_func.Cancel_SendSessionList(chat_id, dayname)

elif (command == "cancel_sessionbyid"):
    # This function is a part of the cancel function
    # This command will cancel a session in appended list data
    # Inputs, DayName, SessionID by int...
    dayName = content.split()[1]
    sessionId = content.split()[2]
    admin_func.CancelSessionById(chat_id, dayName, sessionId)

elif (command == "list"):
    if (queryMode):
         bot.answerCallbackQuery(query_id, "Please wait while we get our shit together.")
    admin_func.list_sess(chat_id, queryMode)

elif (command == "EnterInteractiveMode"): # this is the function that activates the command keybaord...
    admin_func.SendCommandMain(chat_id, "\n *Interactive Mode Enabled* : \n Welcome, please choose a command : ")

elif (command == "raw_list"):
    if (queryMode):
         bot.answerCallbackQuery(query_id, "Please wait while we get our shit together.")
    admin_func.raw_list(chat_id, queryMode)

elif (command == "help"):
    admin_func.help_list(chat_id, queryMode, query_id)

elif (command == "WIP"):
    bot.answerCallbackQuery(query_id, "This function is not ready yet. Try again later.")

elif (command == "disableInteractive"):
    bot.answerCallbackQuery(query_id, "OK, Have a good day.")

elif (command == "send_manipulate_keyboard"):
    admin_func.SendCommandManipulate(chat_id, "Choose command : ")

elif (command == "send_list_keyboard"):
    admin_func.SendCommandList(chat_id, "Choose command : ")



elif (command == "disable_interactive"):
    core.delLastMessage(chat_id)
    bot.sendMessage(chat_id, "Interactive mode disabled. You now have to use command lines. Send /admin to restart interactive mode.", parse_mode="markdown")

else: # fall back clause...
    bot.sendMessage(chat_id, "Command not found. Send `/admin help` for a list of commands", parse_mode="markdown")