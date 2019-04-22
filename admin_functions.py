import sys
import json
import telepot
import traceback
import admin_func_lib as admin_func
import core_functions as core
import respond_function_library as respond_lib
from env import TELEGRAM_BOT_API_KEY
from datetime import datetime
import normie_functions as normie

raw = sys.argv[1]
converted = json.loads(raw)
chat_id = converted["chatId"]
content = converted["content"]
bot = telepot.Bot(TELEGRAM_BOT_API_KEY)

# check if this user is authorised to access the admin
# functions...
if (not core.checkAuthlist(chat_id, "admin")):
    bot.sendMessage(chat_id, "You are not authorised to access this function. Please contact an administrator to get registered as an admin.")
    exit()

if (converted["type"] == "callback_query"):
    # check if the message is
    # callback query or a 
    # normal message
    queryMode = True
    query_id = converted["callbackQueryId"]
else:
    # aaaand the fallback
    # cool? cool cool cool cool
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

print("Command : " + command) # debug the command in the node-red command lines...
user_status_data = core.openJsonFile("user_status_data.json")
awaiting_response_list = user_status_data["awaiting_response_users"]

if (str(chat_id) not in awaiting_response_list):
    # check commands...
    if (command == "list"):

        # this function will send a list of all the session
        # that are set in the long term
        if (queryMode):
            bot.answerCallbackQuery(query_id, "Please wait while we get our shit together.")
        admin_func.list_sess(chat_id, queryMode)

    elif (command == "raw_list"):
        # send a list of all sessions
        # that are set in the long term...
        if (queryMode):
            bot.answerCallbackQuery(query_id, "Please wait while we get our shit together.")
        admin_func.raw_list(chat_id, queryMode)

    elif (command == "help"):
        # send a list of commands available
        admin_func.help_list(chat_id, queryMode, query_id)
        
    elif (command == "EnterInteractiveMode"): 
        # this is the function that activates the command keybaord...
        # will be activated by sending the /admin command alone...
        admin_func.SendCommandMain(chat_id, "\n *Interactive Mode Enabled* : \n Welcome, please choose a command : ")



    else: 
        # fall back clause...
        # every conditional statement should have
        # one... Subscribe to Pewdiepie
        bot.sendMessage(chat_id, "Command not found. Send `/admin help` for a list of commands", parse_mode="markdown")



        
else:
    # fall back if there is a operation to be completed by the user...
    # this is a function because there are other files that use the same opereation...
    # yay
    core.sendCompleteCurrentOperation(chat_id)