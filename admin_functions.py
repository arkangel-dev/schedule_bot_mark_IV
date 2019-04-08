import sys
import json
import telepot
import traceback
import admin_func_lib as admin_func
import core_functions as core
import respond_function_library as respond_lib
from env import TELEGRAM_BOT_API_KEY
from datetime import datetime

raw = sys.argv[1]
converted = json.loads(raw)
chat_id = converted["chatId"]
content = converted["content"]
bot = telepot.Bot(TELEGRAM_BOT_API_KEY)

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


print("Command : " + command) # debug the command in the node-red command lines...

user_status_data = core.openJsonFile("user_status_data.json")
awaiting_response_list = user_status_data["awaiting_response_users"]

if (str(chat_id) not in awaiting_response_list):
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

    elif (command == "revert_cancel_sendlist"):
        # reverts the effects of cancelled session list...
        # used for when reverting the effects of unwanted
        # cancellation of sessions
        admin_func.SendCancelledSessionList(chat_id)

    elif (command == "revert_cancellation"):
        # this function will be used to revert cancellation by
        # day name and the id. Cool? Cool
        dayName = content.split()[1]
        sessionId = content.split()[2]
        admin_func.RevertCancellationById(chat_id, query_id, dayName, sessionId)

    elif (command == "list"):
        # this function will send a list of all the session
        # that are set in the long term
        if (queryMode):
            bot.answerCallbackQuery(query_id, "Please wait while we get our shit together.")
        admin_func.list_sess(chat_id, queryMode)

    elif (command == "EnterInteractiveMode"): 
        # this is the function that activates the command keybaord...
        # will be activated by sending the /admin command alone...
        admin_func.SendCommandMain(chat_id, "\n *Interactive Mode Enabled* : \n Welcome, please choose a command : ")

    elif (command == "raw_list"):
        # send a list of all sessions
        # that are set in the long term...
        if (queryMode):
            bot.answerCallbackQuery(query_id, "Please wait while we get our shit together.")
        admin_func.raw_list(chat_id, queryMode)

    elif (command == "help"):
        # send a list of commands available
        admin_func.help_list(chat_id, queryMode, query_id)

    elif (command == "WIP"):
        # a call backfunction
        # to indicate a function is not ready yet...
        bot.answerCallbackQuery(query_id, "This function is not ready yet. Try again later.")

    elif (command == "disableInteractive"):
        # this will be fall back
        # when the interactive mode
        # is turned off
        bot.answerCallbackQuery(query_id, "OK, Have a good day.")

    elif (command == "send_manipulate_keyboard"):
        # this will send a list of
        # manipulation funtions that you can use
        admin_func.SendCommandManipulate(chat_id, "Choose command : ")

    elif (command == "send_list_keyboard"):
        # this is the main keyboard...
        admin_func.SendCommandList(chat_id, "Choose command : ")

    elif (command == "disable_interactive"):
        # disable the interactive mode...
        # Fun!
        core.delLastMessage(chat_id)
        bot.sendMessage(chat_id, "Interactive mode disabled. You now have to use command lines. Send /admin to restart interactive mode.", parse_mode="markdown")

    elif (command == "append_interactive"):
        core.delLastMessage(chat_id)
        respond_lib.appendStatus_await(chat_id, "append")
        core.appendChat(bot.sendMessage(chat_id, "Please send the data in a good syntax, Send /cancel to cancel this operation"))
    
    else: # fall back clause...
        bot.sendMessage(chat_id, "Command not found. Send `/admin help` for a list of commands", parse_mode="markdown")
        
else:
    # fall back if there is a operation to be completed by the user...
    # this is a function because there are other files that use the same opereation...
    # yay
    core.sendCompleteCurrentOperation(chat_id)