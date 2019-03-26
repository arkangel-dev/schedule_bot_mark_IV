# Misc Functions
import json
from datetime import datetime
from env import TELEGRAM_BOT_API_KEY
import sys
import telepot


# {'message_id': 2137, 'from': {'id': 641334893, 'is_bot': True, 'first_name': 'F.R.I.D.A.Y', 'username': 'FridayHelpBot'
#     }, 'chat': {'id': 488976797, 'first_name': 'Sam', 'last_name': 'Ramirez', 'username': 'IS4AM', 'type': 'private'
#     }, 'date': 1553597500, 'text': 'Hello World'
# }

def appendChat(raw_json):

    message_id = raw_json["message_id"]
    chat_id = raw_json["chat"]["id"]

    f = open("message_ledger.json" , "r")
    file_json = f.read()
    message_ledger = json.loads(file_json)

    message_id = int(message_id)
    dataStruct = message_id

    if (str(chat_id) in message_ledger["chats"]):
         message_ledger["chats"][str(chat_id)].append(dataStruct)
    else:
       # message_ledger["chats"].append(int(chat_id))
        message_ledger["chats"].update({chat_id: []})
        message_ledger["chats"][chat_id].append(dataStruct)
        print(message_ledger)

    with open('message_ledger.json', 'w') as outfile: # save the file
       json.dump(message_ledger, outfile)

def getLastMessage(chat_id):
    f = open("message_ledger.json" , "r")
    file_json = f.read()
    message_ledger = json.loads(file_json)

    if (str(chat_id) in message_ledger["chats"]):
        messageList = message_ledger["chats"][str(chat_id)]
        if (len(messageList) != 0):
            return(max(messageList))
        else:
            return(None)
    else:
        return(None)

def delLastMessage(chat_id):
    bot = telepot.Bot(TELEGRAM_BOT_API_KEY)
    last_id = getLastMessage(chat_id)
    if (last_id != None):
        try:
            bot.deleteMessage((chat_id, last_id))
        except:
            # bot.sendMessage(chat_id, "ERR: Message Not Found!")
            print("ERR : Message not found!")

