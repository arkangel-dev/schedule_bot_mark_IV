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

print("[!] Incoming : " + str(chat_id) + " (" + core.getUserDetails(chat_id)["username"] + ")") 
print("[!] Content (KEYBOARD) : " + content)


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
    if (command == "append"):
        # append the sessions to the
        # main sessions list system
        admin_func.append_session(chat_id, content)
        core.checkAuthMessage(chat_id)

    elif (command == "cancel_session"):
        # This function is a part of the cancel functions...
        # this command will send a list of all the days
        # from which you can send one to cancel that
        # day's session(s)
        core.checkAuthMessage(chat_id)
        admin_func.Cancel_SendDayList(chat_id)
        

    elif (command == "EnterInteractiveMode"): 
        # this is the function that activates the command keybaord...
        # will be activated by sending the /admin command alone...
        core.checkAuthMessage(chat_id)
        admin_func.SendCommandMain(chat_id, "\n *Interactive Mode Enabled* : \n Welcome, please choose a command : ")

    elif (command == "send_manipulate_keyboard"):
        # this will send a list of
        # manipulation funtions that you can use
        core.checkAuthMessage(chat_id)
        if core.checkAuthlist(chat_id, "admin"):
            admin_func.SendCommandManipulate(chat_id, "Choose command : ")
        else:
            bot.sendMessage(chat_id, "It seems you are not an admin to a class. Please add your self to one to control it.")
            admin_func.SendCommandMain(chat_id, "Null")

    elif (command == "cancel_getsessionid"):
        # This function is part of the cancel function
        # This command will send a list of all sessions
        # on that day...
        # inputs : DayName
        core.checkAuthMessage(chat_id)
        dayname = content.split()[1]
        admin_func.Cancel_SendSessionList(chat_id, dayname)

    elif (command == "cancel_sessionbyid"):
        # This function is a part of the cancel function
        # This command will cancel a session in appended list data
        # Inputs, DayName, SessionID by int...
        core.checkAuthMessage(chat_id)
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
        core.checkAuthMessage(chat_id)
        dayName = content.split()[1]
        sessionId = content.split()[2]
        admin_func.RevertCancellationById(chat_id, query_id, dayName, sessionId)

    elif (command == "list"):
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

    elif (command == "WIP"):
        # a call backfunction
        # to indicate a function is not ready yet...
        bot.answerCallbackQuery(query_id, "This function is not ready yet. Try again later.")

    elif (command == "send_list_keyboard"):
        # this is the main keyboard...
        core.checkAuthMessage(chat_id)
        admin_func.SendCommandList(chat_id, "Choose command : ")

    elif (command == "corefunctionkeyboard"):
        # this function is used to send a keyboard for the core functions.
        # this will aslo be filtered from a list of authorised list
        core.checkAuthMessage(chat_id)
        admin_func.sendCoreFunctKeyboard(chat_id)

    elif (command == "help"):
        # send a list of commands available
        admin_func.admin_help_list(chat_id, queryMode, query_id)

    elif (command == "register"):
        # send a keyboard so the user can register
        # their account to a programme
        normie.registerUser(chat_id, content)


    elif (command == "disable_interactive"):
        # disable the interactive mode...
        # Fun!
        core.checkAuthMessage(chat_id)
        core.delLastMessage(chat_id)
        bot.sendMessage(chat_id, "Interactive mode disabled. You now have to use command lines. Send /admin to restart interactive mode.", parse_mode="markdown")

    elif (command == "append_interactive"):
        # this is the function to appened sessions
        # via interactive mode...
        core.delLastMessage(chat_id)
        respond_lib.appendStatus_await(chat_id, "append_session")
        core.appendChat(bot.sendMessage(chat_id, "*Append Session : * \nPlease send the session details in the appropriate syntax. Type /help to view the syntax \nSend /cancel to cancel this operation", parse_mode="markdown"))

    elif (command == "admin_add"):
        # this function is used to add mid level admins
        # to the system. These admins have limted authority
        # over editing the sessions of the system
        admin_func.admin_add(chat_id, content)

    elif (command == "admin_revoke"):
        # this function is used to revoke the authority that
        # was not meant to be given to power hungry users.
        # Always have kill function... always
        admin_func.admin_revoke(chat_id, content)

    elif (command == "h_admin_add"):
        # not its time to add a higher core admin...
        admin_func.h_admin_add(chat_id, content)

    elif (command == "update_otp"):
        # ok so this is the function to update the otp
        # qr code because a core admin fucked up and leaked
        # his otp key somehow...
        admin_func.updateOtpCodes(chat_id)
        

    else:
        bot.sendMessage(chat_id, "⚠️ Button check for '" + command + "' is not programmed in yet ⚠️")


else:
    # fall back if there is a operation to be completed by the user...
    # this is a function because there are other files that use the same opereation...
    # yay
    core.sendCompleteCurrentOperation(chat_id)