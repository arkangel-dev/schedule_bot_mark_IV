import time
import sys
import json
import core_functions as core
import telepot
import env
import traceback

# @todo Clean up manipulate_payload.py
# @body The payload file is bare bones for the system to work.; Needs more work
# So the question is, How the fuck does this file work? So in the node-red
# Workflow the a new key is added to the payload. This file will add said 
# key. The purpose of this key is irrelevent to be explained in this file... :p

bot = telepot.Bot(env.TELEGRAM_BOT_API_KEY)

payload_raw = sys.argv[1]
payload = json.loads(payload_raw)
chat_id = payload["chatId"]
content = payload["content"]

status_data = core.openJsonFile("user_status_data.json")

user_list = core.openJsonFile("user_list.json")

try:
    username = core.getUserDetails(chat_id)["username"]
except:
    bot.sendChatAction(chat_id, "typing")
    bot.sendMessage(chat_id, "No username, No service. Get a username and then we'll talk or else get lost!")
    bot.sendSticker(chat_id, "CAADAQADJwADLRrhIITCggTyx2NsAg")
    exit()


if not str(chat_id) in user_list["users"]:
    username = core.getUserDetails(chat_id)["username"]
    user_list["users"].update({str(chat_id):[]})
    user_list["users"][str(chat_id)].append(username)
    core.saveJsonFile(user_list, "user_list.json")

if (str(chat_id) in status_data["awaiting_response_users"]):
    # if the system is expecting an input from this user
    # enter the awaiting data with the value as True
    payload.update({"awaiting_data" : True })
else:
    # or else enter it as false
    payload.update({"awaiting_data" : False })

# print the modified payload
print(json.dumps(payload))