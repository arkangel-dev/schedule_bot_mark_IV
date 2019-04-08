# Misc Functions
import json
from datetime import datetime
from env import TELEGRAM_BOT_API_KEY
import sys
import telepot
import traceback


# {'message_id': 2137, 'from': {'id': 649384853, 'is_bot': True, 'first_name': 'F.R.I.D.A.Y', 'username': 'ItsFuckingFriday'
#     }, 'chat': {'id': 438938797, 'first_name': 'David', 'last_name': 'Bowie', 'username': 'PoopyButthole', 'type': 'private'
#     }, 'date': 1553597500, 'text': 'Hello World'
# }

def openJsonFile(filename):
    # open the json file...
    try:
        f = open(filename , "r")
        file_json = f.read()
        return_value = json.loads(file_json)
        return(return_value)
    except:
        print("Operation error while opening file : " + filename)
        exit()

def saveJsonFile(data, filename):
    try:
        with open(filename, 'w') as outfile: # save the file
            json.dump(data, outfile)
    except:
        print("Operation error while saving file")
        exit()

def appendChat(raw_json):
    # this function will add a message id
    # to each chat id in the json file so
    # that the keyboards can be deleted later...
    # used for suicidal keyboards
    message_id = raw_json["message_id"]
    chat_id = raw_json["chat"]["id"]
    f = open("message_ledger.json" , "r")
    file_json = f.read()
    message_ledger = json.loads(file_json)
    message_id = int(message_id)
    dataStruct = message_id

    if (str(chat_id) in message_ledger["chats"]):
        message_ledger["chats"][str(chat_id)] = []
        message_ledger["chats"][str(chat_id)].append(dataStruct)
    else:
       # message_ledger["chats"].append(int(chat_id))
        message_ledger["chats"].update({chat_id: []})
        message_ledger["chats"][chat_id].append(dataStruct)
        print(message_ledger)

    with open('message_ledger.json', 'w') as outfile: # save the file
       json.dump(message_ledger, outfile)

def getLastMessage(chat_id):
    # this function will return the
    # last keyboard the bot has sent.
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
    # this function will delete the previous
    # keyboard from the chat. It does so
    # by getting the latest keyboard ID from
    # the message ledger and deleting it
    bot = telepot.Bot(TELEGRAM_BOT_API_KEY)
    last_id = getLastMessage(chat_id)
    if (last_id != None):
        try:
            bot.deleteMessage((chat_id, last_id))
        except:
            bot.sendMessage(chat_id, "ERRx001 : (The specified keyboard was not found)")
            print("ERR : Message not found : (The specified keyboard was not found)")

