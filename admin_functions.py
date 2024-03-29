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

print("[!] Incoming : " + str(chat_id) + " (" + core.getUserDetails(chat_id)["username"] + ")") 
print("[!] Content : " + content)
bot = telepot.Bot(TELEGRAM_BOT_API_KEY)
#
# send the request to telegram to send
# the 'typing...' status to the 
# user. This will make delays in send the
# responses more natural
#
bot.sendChatAction(chat_id, "typing")

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
        admin_func.admin_help_list(chat_id, queryMode, query_id)
        
    elif (command == "EnterInteractiveMode"): 
        # this is the function that activates the command keybaord...
        # will be activated by sending the /admin command alone...
        core.checkAuthMessage(chat_id)
        admin_func.SendCommandMain(chat_id, "\n *Interactive Mode Enabled* : \n Welcome, please choose a command : ")

    elif (command == "verify-otp"):
        # so this function will be used to verify the OTP code of the user
        # without completing a core function
        admin_func.verifyOtp(chat_id, content)

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