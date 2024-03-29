import sys
import json
import core_functions as core
import env
import telepot
import respond_function_library as respond_lib


bot = telepot.Bot(env.TELEGRAM_BOT_API_KEY)
raw = sys.argv[1]
converted = json.loads(raw)
chat_id = converted["chatId"]
content = converted["content"]
bot.sendChatAction(chat_id, "typing")

user_status_data = core.openJsonFile("user_status_data.json")
awaiting_response_list = user_status_data["awaiting_response_users"]
callbackfuntion = awaiting_response_list[str(chat_id)]["callback_function"]

if (content.split()[0] == "/cancel"):

    # check if this user is trying to cancel
    # the currrent operation.
    bot.sendMessage(chat_id, "*Cancelling Operation : * \nOperation has been cancelled. Is there anything else you want me to do?", parse_mode="markdown")
    respond_lib.deleteStatus_await(chat_id)
    # do not comment ^ this out
    # because without it there is no
    # way to break out of an infinite
    # input request

if (content.split()[0][0] == "/") and (content.split()[0] != "/done"):
    # see if the user is trying
    # execute a command...
    core.sendCompleteCurrentOperation(chat_id)
    exit() # be sure to exit. or else things can get messy


# aight, lets go over how this will work.
# when the user invokes a function that require
# further input the userstatus data will be updated,
# indicating that the system is expecting an input from
# the user. 

# if the user enters an input that is not acceptable then
# the bot will send back a message saying the data is not acceptable
# this is done by the admin_function.py file. It will check the user_status_data file
# to check if any input is expected
# to check if the input is usable by the function
# it will sent to another function library file... (respond_function_library.py)

# if the user enters valid input then the system will delete the user's entry
# in the status file.

# first lets make the append session function for
# the await input method. I hope this works...

if (callbackfuntion == "append_session"):
    respond_lib.appendSession_enter(chat_id, content)

elif (callbackfuntion == "admin_add"):
    respond_lib.admin_add(chat_id, content)

elif (callbackfuntion == "h_admin_add"):
    respond_lib.h_admin_add(chat_id, content)