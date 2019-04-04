import sys
import json
import telepot
from env import TELEGRAM_BOT_API_KEY
from datetime import datetime
import traceback
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import core_functions as core
import time
import parse_data as parsedata


# open the append-session file...
f = open("appended_sessions_list.json" , "r")
file_json = f.read()
append_raw_data = json.loads(file_json)

# open the main session file...
f = open("session_list.json" , "r")
file_json = f.read()
session_raw_data = json.loads(file_json)

bot = telepot.Bot(TELEGRAM_BOT_API_KEY)
af_version = 0.75

# ####################################################################################
# ####################################################################################

def list_sess(chat_id, query_mode):
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
    if (query_mode):
        SendCommandMain(chat_id, "\n *Interactive Mode Enabled* : \n Welcome, please choose a command : ")

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

def raw_list(chat_id, query_mode):
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
    if (query_mode):
        SendCommandMain(chat_id, "\n *Interactive Mode Enabled* : \n Welcome, please choose a command : ")

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
        SendCommandMain(chat_id, "\n *Interactive Mode Enabled* : \n Welcome, please choose a command : ")

# ####################################################################################
# ####################################################################################

# def cancelSession(chat_id, arguments):
#     # the arguments will be Day, SessionID
#     x = None

# ####################################################################################
# ####################################################################################

# ["SESSION_NAME", "STARTING_TIME", "ENDING_TIME", "BRING_LAPTOP_BOOLEAN", "LECTURER_NAME", "VENUE"]
# ATHFAN'S CODE
#=========================================================================
# import telepot
# from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

# keyboard = InlineKeyboardMarkup(inline_keyboard=[
#                    [InlineKeyboardButton(text="hey", callback_data='/command1')],
#                    [InlineKeyboardButton(text="hey", callback_data='/command1')],
#                    [InlineKeyboardButton(text="hey", callback_data='/command1')]
#                ])

# bot = telepot.Bot("641334893:AAF1_MJ2ou9nGt4MIbAYSIWMUxfKPDCpDAw")
# bot.sendMessage(488976797, "Hello", reply_markup = keyboard)
#===========================================================================

def SendCommandList(chat_id, content):
    # this is the keyboard that will be sent to the user when the list command is sent from the
    # main keyboard...
    keyboard = InlineKeyboardMarkup(inline_keyboard=[ # define the inline keyboard before we can use it...
                        [InlineKeyboardButton(text="List main sessions", callback_data='raw_list')],
                        [InlineKeyboardButton(text="List temporary manipulations", callback_data='list')],
                        [InlineKeyboardButton(text="« Cancel", callback_data='EnterInteractiveMode')]
                   ])
    core.delLastMessage(chat_id)
    core.appendChat(bot.sendMessage(chat_id, "*List Sessions : * \nSelect a command : ", reply_markup = keyboard, parse_mode="markdown"))

def SendCommandManipulate(chat_id, content):
    # this the function that will be sent to the uesr when the manipulate function is
    # invoked from the main keyboard...
    keyboard = InlineKeyboardMarkup(inline_keyboard=[ # define the inline keyboard before we can use it...
                        [InlineKeyboardButton(text="Cancel Session", callback_data="cancel_session"),
                        InlineKeyboardButton(text="Append Session", callback_data="WIP")],
                        [InlineKeyboardButton(text="Revert Cancelled", callback_data="WIP"),
                        InlineKeyboardButton(text="Cancel Appended", callback_data="WIP")],
                        [InlineKeyboardButton(text="« Cancel", callback_data='EnterInteractiveMode')]
                   ])
    core.delLastMessage(chat_id)
    core.appendChat(bot.sendMessage(chat_id, "*Cancel Session :* \nSelect a command : ", reply_markup = keyboard, parse_mode="markdown"))

def SendCommandMain(chat_id, content):
    # override the content variable
    content = "*Main Menu : * \nPlease select a command to continue : "
    # this is the function that will be sent to the user when the /admin function is
    # first invoked...
    keyboard = InlineKeyboardMarkup(inline_keyboard=[ # define the inline keyboard before we can use it...
                        [InlineKeyboardButton(text="List Sessions", callback_data='send_list_keyboard')],
                        [InlineKeyboardButton(text="Manipulate Sessions", callback_data="send_manipulate_keyboard")],
                        [InlineKeyboardButton(text="Call for help", callback_data='help')],
                        [InlineKeyboardButton(text="« Exit Interactive Mode", callback_data="disable_interactive")]
                   ])
    core.delLastMessage(chat_id)
    core.appendChat(bot.sendMessage(chat_id, content, reply_markup = keyboard, parse_mode="markdown"))

def Cancel_SendSessionList(chat_id, DayName):
    # send a list of keyboard button containing
    # all the session of a day that is specified
    # as an argument...
    session_count = parsedata.getSessionCount(DayName)

    if (session_count != 0):
        keyboard = []
        for sessionid in range(0,session_count):
            # run this loop for each session
            # the loop runs from 0 to session_count
            # parse a the details of the sessions
            # so the data can be parsed into a keyboard
            data = parsedata.parseSessionData(sessionid, DayName.lower())
            session_name    = data[0]
            session_start   = data[1]
            session_end     = data[2]
            lecturer        = data[4]
            venue           = data[5]
            
            keyboard_text = session_name + " | From " + str(session_start) + " to " + str(session_end) + " | " + lecturer + " | " + venue
            callback_text = "cancel_sessionbyid " + " " + str(DayName.lower()) + " " + str(sessionid)  # create a command callback system
            keyboard.append([InlineKeyboardButton(text=keyboard_text, callback_data=callback_text)])  # append the keyboard button into the keyboard
            # Make the send the keyboard

        keyboard.append([InlineKeyboardButton(text="« Go Back", callback_data='cancel_session')])
        SendCustomKeyboard(chat_id, "*Cancel Session : * \nPlease select a session from the list below to cancel it : ", keyboard)
        # add the cancel button
    else:
        # if there are no session say that
        # there are no sessions in the the content
        # of the keyboard
        keyboard = []
        keyboard.append([InlineKeyboardButton(text="« Go Back", callback_data='cancel_session')])
        SendCustomKeyboard(chat_id, "*Cancel Session : * \nYou have no sessions on the selected day : ", keyboard)
       
def Cancel_SendDayList(chat_id):
    # send the day list so that the user can
    # choose a day and recieve a session list
    keyboardList = [
        [InlineKeyboardButton(text="Sunday", callback_data='cancel_getsessionid Sunday'),
        InlineKeyboardButton(text="Monday", callback_data='cancel_getsessionid Monday')],
        [InlineKeyboardButton(text="Tuesday", callback_data='cancel_getsessionid Tuesday'),
        InlineKeyboardButton(text="Wednesday", callback_data='cancel_getsessionid Wednesday')],
        [InlineKeyboardButton(text="Thursday", callback_data='cancel_getsessionid Thursday'),
        InlineKeyboardButton(text="Friday", callback_data='cancel_getsessionid Friday')],
        [InlineKeyboardButton(text="Saturday", callback_data='cancel_getsessionid Saturday')],
        [InlineKeyboardButton(text="« Cancel", callback_data='EnterInteractiveMode')],
    ]
    
    SendCustomKeyboard(chat_id, "*Cancel Session :* \nSelect a day :", keyboardList)

def CancelSessionById(chat_id, DayName, session_id):
    # function to send modify the session list
    # so that the session will be cancelled...
    bot.sendMessage(chat_id, "*Status Return : * \n" + DayName + "'s session ID " + session_id + " has been cancelled. A blast out will be sent out in a few minutes.", parse_mode="markdown")
    SendCommandMain(chat_id, "Null Data")
    append_raw_data["cancelled"][DayName].append(session_id)
    with open('appended_sessions_list.json', 'w') as outfile: # save the file
        json.dump(append_raw_data, outfile)

def SendCustomKeyboard(chat_id, content, commands):
    # send a custom keyboard with custom commands
    # the commands will have to be sent as an array...
    keyboard = InlineKeyboardMarkup(inline_keyboard=commands)
    core.delLastMessage(chat_id)
    core.appendChat(bot.sendMessage( chat_id, content, reply_markup=keyboard, parse_mode="markdown"))



