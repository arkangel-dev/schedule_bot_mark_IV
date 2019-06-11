# Misc Functions
import json
from datetime import datetime
from env import TELEGRAM_BOT_API_KEY
import sys
import telepot
import traceback
import ast, re
from contextlib import contextmanager
import sys, os


# {'message_id': 2137, 'from': {'id': 649384853, 'is_bot': True, 'first_name': 'F.R.I.D.A.Y', 'username': 'ItsFuckingFriday'
#     }, 'chat': {'id': 438938797, 'first_name': 'David', 'last_name': 'Bowie', 'username': 'PoopyButthole', 'type': 'private'
#     }, 'date': 1553597500, 'text': 'Hello World'
# }

bot = telepot.Bot(TELEGRAM_BOT_API_KEY)


# sometimes to supress the output
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

def openJsonFile(filename):
    # open the json file...
    # pretty explanatory...
    try:
        # try to open this file
        f = open(filename , "r")
        file_json = f.read()
        return_value = json.loads(file_json)
        return(return_value)
    except:
        # if it all goes south
        # mostly by absent files
        # or non valid data in said files
        print("Operation error while opening file : " + filename)
        exit()

def saveJsonFile(data, filename):
    # this is the save counterpart for
    # the openJsonFile() function
    # Yay!
    try:
        with open(filename, 'w') as outfile: # save the file
            json.dump(data, outfile)
    except:
        print("Operation error while saving file to disk : " + filename)
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

    last_id = getLastMessage(chat_id)
    if (last_id != None):
        try:
            bot.deleteMessage((chat_id, last_id))
        except:
            # bot.sendMessage(chat_id, "ERRx001 : (The specified keyboard was not found)")
            print("ERR : Message not found : (The specified keyboard was not found)")

def sendCompleteCurrentOperation(chat_id):
    # this is what is supposed to be done when
    # user tries to execute commands when the 
    # system is expecting input from the user...
    bot.sendMessage(chat_id, "Please complete current operation. If you dont want to complete this operation send /cancel and get this over with. I have places to be.")

def checkAuthlist(chat_id, list_name):
    # this function will accept a chat_id and a list
    # that will return if a user is authorised...
    authList = openJsonFile("auth_list.json")
    subList = authList[list_name]
    if (str(chat_id) in subList):
        return(True)
    else:
        return(False)

def checkAuthMessage(chat_id):
    # check if this user is authorised to access the admin
    # functions...
    if not (checkAuthlist(chat_id, "admin") or checkAuthlist(chat_id, "core_admin")):
        bot.sendMessage(chat_id, "You are not authorised to access this function. Please contact an administrator to get registered as an admin.")
        exit()

def getUserDetails(chat_id):
    return(bot.getChat(chat_id))

def lookUpUser(username, add_buffer=False):
    raw_user_list = openJsonFile("user_list.json")
    for x in raw_user_list["users"]:
        if raw_user_list["users"][x][0] == username:
            if (add_buffer):
                return("Null ," + x)
            else:
                return(x)
    return(False)

def sendImg(chat_id, file):
	bot.sendPhoto(chat_id, open(file, 'rb'))

def getDataType(str):
    str=str.strip()
    if len(str) == 0: return 'BLANK'

    if re.match(r'True$|^False$|^0$|^1$', str):
        return 'bit'
    if re.match(r'([-+]\s*)?\d+[lL]?$', str): 
        return 'integer'
    if re.match(r'([-+]\s*)?[1-9][0-9]*\.?[0-9]*([Ee][+-]?[0-9]+)?$', str): 
        return 'float'
    if re.match(r'([-+]\s*)?[0-9]*\.?[0-9][0-9]*([Ee][+-]?[0-9]+)?$', str): 
        return 'float'

    return 'text' 