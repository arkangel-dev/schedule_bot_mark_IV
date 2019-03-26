import sys
import json
import telepot
from env import TELEGRAM_BOT_API_KEY
from datetime import datetime
import traceback

# open the append-session file...
f = open("test_json.json" , "r")
file_json = f.read()
append_raw_data = json.loads(file_json)

# open the main session file...
f = open("session_list.json" , "r")
file_json = f.read()
session_raw_data = json.loads(file_json)

bot = telepot.Bot(TELEGRAM_BOT_API_KEY)
af_version = 0.5

# ####################################################################################
# ####################################################################################

def list_sess(chat_id):
    #
    # List command
    # invoked by /list
    # any additional arugemnts are ignored
    #
    session_list = []
    day_list = ("monday","tuesday","wednesday","thursday","friday","saturday","sunday")

    session_list.append("*Appended Sessions : * \n")
    for x in day_list:
        session_list.append(x + " : \n")
        if len(append_raw_data["appended"][x]) != 0:
            count = 0
            for y in append_raw_data["appended"][x]:
                session_list.append("`" + str(count) + " : " + str(y) + "`\n")
                count += 1

    session_list.append("\n *Cancelled Sessions : * \n")
    for x in day_list:
        session_list.append(x + " : \n")
        if len(append_raw_data["cancelled"][x]) != 0:
            count = 0
            for y in append_raw_data["cancelled"][x]:
                session_list.append("`" + str(count) + " : " + str(y) + "`\n")
                count += 1
    finalString = ""
    for x in session_list:
        finalString += x
    bot.sendMessage(chat_id, finalString, parse_mode="markdown")

# ####################################################################################
# ####################################################################################

def append_session(chat_id, content):
    #
    # The argument syntax should be as the following...
    # append day,session_name,start_time,end_time,bring_laptop,lecturer_name,venue
    #
    try: # check if there are any errors
        arguments = (content.split()[1]).split(",")
        dataStuct_str = arguments[1] + "," + arguments[2] + "," + arguments[3] + "," + arguments[4] + "," + arguments[5] + "," + arguments[6] # create the data structure
        dataStuct = dataStuct_str.split(",") # convert the string data structure to a list
        append_raw_data["appended"][arguments[0]].append(dataStuct) # append that list to the set date
        with open('test_json.json', 'w') as outfile: # save the file
            json.dump(append_raw_data, outfile)
        bot.sendMessage(chat_id, "Session appended to " + arguments[0] + " as the set [" + dataStuct_str + "]")
    except Exception: # fall back for the errors : Can only be triggered by a bad request
        bot.sendMessage(chat_id, "ERROR : Malformed argument set reciveved")

# ####################################################################################
# ####################################################################################

def raw_list(chat_id):
    #
    # print out the session list
    #
    session_list = []
    session_list.append("*Main Long Term List* \n")
    day_list = ("monday","tuesday","wednesday","thursday","friday","saturday","sunday")
    for x in day_list:
        session_list.append(x + " : \n")
        if (len(session_raw_data["days"][x]["sessions"]) != 0):
            count = 0
            for y in session_raw_data["days"][x]["sessions"]:
                session_list.append(str(count) + " : `" + str(y) + "` \n")
                count += 1

    finalString = ""
    for x in session_list:
        finalString += x
    bot.sendMessage(chat_id, finalString, parse_mode="markdown")

# ####################################################################################
# ####################################################################################

def help_list(chat_id, query_mode, query_id):
    #
    # Help command...
    # Invoked by /append help
    # any additional arguments are ignored
    #
    outputList = [] # create the help Lists
    outputList.append("*HELP* \n\n")

    outputList.append("*Append : * \n")
    outputList.append("Adds a temporary session to the agenda. \n")
    outputList.append("Use as : ` /admin append DAY,SESSION_NAME,STARTING_TIME,ENDING_TIME,BRING_LAPTOP_BOOLEAN,LECTURER_NAME,VENUE` \n\n")

    outputList.append("*List : * \n")
    outputList.append("Lists all the appended session data stored. \n")
    outputList.append("Use as : ` /admin list `\n\n")

    outputList.append("*Raw List : * \n")
    outputList.append("Lists all the long term sessions. Useful for cancelling sessions. \n")
    outputList.append("Use as : ` /admin raw_list `\n\n")


    outputList.append("*Help : * \n")
    outputList.append("Sends help. That's all it does. \n")
    outputList.append("Use as : ` /admin help`")

    outputList.append("\n\n `Admin Functions Version : " + str(af_version) + "`")

    # convert it to a single string...
    finalString = ""
    for x in outputList:
        finalString += x
    bot.sendMessage(chat_id, finalString, parse_mode="markdown") # enable markdown and send it...

    if (query_mode):
        bot.answerCallbackQuery(query_id , "Here's your help. Have a good day")

# ####################################################################################
# ####################################################################################

def SendCommandKeyboard(chat_id, content):
    from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

    keyboard = InlineKeyboardMarkup(inline_keyboard=[ # define the inline keyboard before we can use it...
                        [InlineKeyboardButton(text="List main sessions", callback_data='raw_list')],
                        [InlineKeyboardButton(text="List temporary manipulations", callback_data='list')],
                        [InlineKeyboardButton(text="Call for help", callback_data='help')],
                        [InlineKeyboardButton(text="Cancel", callback_data='disableInteractive')]
                   ])

    bot = telepot.Bot(TELEGRAM_BOT_API_KEY)
    bot.sendMessage(chat_id, content, reply_markup = keyboard, parse_mode="markdown")