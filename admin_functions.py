import sys
import json
import telepot
from env import TELEGRAM_BOT_API_KEY
from datetime import datetime
import traceback
# ["SESSION_NAME", "STARTING_TIME", "ENDING_TIME", "BRING_LAPTOP_BOOLEAN", "LECTURER_NAME", "VENUE"]

raw = sys.argv[1]
converted = json.loads(raw)
chat_id = converted["chatId"]
content = converted["content"]
command = content.split()[0]
arguments = (content.split()[1]).split(",")
bot = telepot.Bot(TELEGRAM_BOT_API_KEY)

# debug the command in the node-red command lines...
print("Command : " + command)

# open the append-session file...
f = open("test_json.json" , "r")
file_json = f.read()
raw_data = json.loads(file_json)

# check commands...
if (command == "append"): # append_sessions...
    #
    # The argument syntax should be as the following...
    # append day,session_name,start_time,end_time,bring_laptop,lecturer_name,venue
    #
    try:
        dataStuct_str = arguments[1] + "," + arguments[2] + "," + arguments[3] + "," + arguments[4] + "," + arguments[5] + "," + arguments[6] # create the data structure
        dataStuct = dataStuct_str.split(",") # convert the string data structure to a list
        raw_data["appended"][arguments[0]].append(dataStuct) # append that list to the set date
        with open('test_json.json', 'w') as outfile: # save the file
            json.dump(raw_data, outfile)
        bot.sendMessage(chat_id, "Session appended to " + arguments[0] + " as the set [" + dataStuct_str + "]")
    except Exception:
        bot.sendMessage(chat_id, "ERROR : Malformed argument set reciveved")
else: # fall back clause...
    bot.sendMessage(chat_id, "Command not found...", parse_mode="markdown")


