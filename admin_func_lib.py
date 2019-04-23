import sys
import json
import telepot
import traceback
import core_functions as core
import time
import parse_data as parsedata
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from env import TELEGRAM_BOT_API_KEY
from env import BUILD_ID
import env


    

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
        append_raw_data = core.openJsonFile("appended_sessions_list.json")
        arguments = content[7:len(content)].split(",")
        print(arguments)
        dataStuct_str = arguments[1] + "," + arguments[2] + "," + arguments[3] + "," + arguments[4] + "," + arguments[5] + "," + arguments[6] # create the data structure
        dataStuct = dataStuct_str.split(",") # convert the string data structure to a list
        append_raw_data["appended"][arguments[0].lower()].append(dataStuct) # append that list to the set date
        core.saveJsonFile(append_raw_data, "appended_sessions_list.json")
        bot.sendMessage(chat_id, "Session appended to *" + arguments[0].capitalize() + "* as the set `[" + dataStuct_str + "]`", parse_mode="markdown")
        return(1)
    except Exception: # fall back for the errors : Can only be triggered by a bad request
        bot.sendMessage(chat_id, "ERROR : Malformed argument set reciveved")
        return(0)
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
        session_list.append(x.capitalize() + " : \n")
        if (len(session_raw_data["days"][x]["sessions"]) != 0):
            count = 0
            for y in session_raw_data["days"][x]["sessions"]:
                session_list.append(str(count))
                session_list.append("`   Session : " + y[0] + "\n    Start Time : " + y[1] + "\n    End Time : " + y[2] + "\n    Venue : " + y[5] + "`\n")
                count += 1

    finalString = ""
    for x in session_list:
        finalString += x
    bot.sendMessage(chat_id, finalString, parse_mode="markdown")
    if (query_mode):
        SendCommandMain(chat_id, "\n *Interactive Mode Enabled* : \n Welcome, please choose a command : ")

# ####################################################################################
# ####################################################################################

def admin_help_list(chat_id, query_mode = False, query_id = 0):
    #
    # Help command...
    # Invoked by /append help
    # any additional arguments are ignored
    #
    outputList = [] # create the help Lists
    outputList.append("*Help & Support (For Admins)* \n\n")
    #outputList.append("*Intoduction* : \nAs long as technology existed there existed folks who didn't know squat about said technology. So a group high minded interllectuals gathered and came up with the concept of the documentation. They wrote documentation for every piece of innovation they made. They even made a tutorial on how to lift up a chair. So anyway, the backend development of a telegram bot is pretty new to me and the code is pretty weird. So naturally me (@ArkangelDev) and Ice Bear (@athfan) had to create a documentation for this. But our documentation is pretty weird. Also we have a weird sense of humor and thus this un-nessesarily looong text. Soo yeah, you wasted 3 minutes reading this.\n\n")
    outputList.append("*Append session* :  \nTo append a session click manipulate sessions on the main keyboard, from there click on append session. And send the details of the session when requested. The details have to be syntaxed in the following way : _Day Name, Session Name, Start Time, End Time, Bring Laptop Boolean, Professor Name, Venue_ \n\n")
    outputList.append("*Cancel Session* :  \nTo cancel a session, click on manipluate session on the main keyboard, from here click on cancel session, then you are presented with a list of days. Select a day and you'll be presented with a list of sessions. Click on a session to cancel it. \n\n")
    outputList.append("*Revert Cancellation* : \nTo revert the effect of cancellation of sessions, click on manipulate sessions on the main keyboard. From here select Revert Cancellation and you'll be presented with a list of cancelled sessions. Click on one of them to revert the cancellation effect.\n\n")
    outputList.append("*Revert Appending* : \nTo revert an appended session. This function is not ready yet... So yeah... Subscribe to PewDiePie! \n\n")
    outputList.append("`Admin Functions Version : " + str(env.ADMIN_BUILD_ID) + "`")
    outputList.append("\n`Development Version : " + str(BUILD_ID) + "`")
    outputList.append("\n`Created and Hosted by @ArkangelDev, @athfan`")

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
                        [InlineKeyboardButton(text="Cancel", callback_data='EnterInteractiveMode')]
                   ])
    core.delLastMessage(chat_id)
    core.appendChat(bot.sendMessage(chat_id, "*List Sessions : * \n Select a command : ", reply_markup = keyboard, parse_mode="markdown"))

def SendCommandManipulate(chat_id, content):
    # this the function that will be sent to the uesr when the manipulate function is
    # invoked from the main keyboard...
    keyboard = InlineKeyboardMarkup(inline_keyboard=[ # define the inline keyboard before we can use it...
                        [InlineKeyboardButton(text="Cancel Session", callback_data="cancel_session"),
                        InlineKeyboardButton(text="Append Session", callback_data="append_interactive")],
                        [InlineKeyboardButton(text="Revert Cancelled", callback_data="revert_cancel_sendlist"),
                        InlineKeyboardButton(text="Cancel Appended", callback_data="WIP")],
                        [InlineKeyboardButton(text="Cancel", callback_data='EnterInteractiveMode')]
                   ])
    core.delLastMessage(chat_id)
    core.appendChat(bot.sendMessage(chat_id, "*Manipulate Session :* \nSelect a command : ", reply_markup = keyboard, parse_mode="markdown"))

def SendCommandMain(chat_id, content):
    # override the content variable
    content = "*Admin Main Menu : * \nPlease select a command to continue : "
    # this is the function that will be sent to the user when the /admin function is
    # first invoked...
    keyboard = InlineKeyboardMarkup(inline_keyboard=[ # define the inline keyboard before we can use it...
                        [InlineKeyboardButton(text="List Sessions", callback_data='send_list_keyboard'),
                        InlineKeyboardButton(text="Manipulate Sessions", callback_data="send_manipulate_keyboard")],
                        [InlineKeyboardButton(text="Send out blast", callback_data='WIP'),
                        InlineKeyboardButton(text="Core Settings", callback_data="corefunctionkeyboard")],
                        [InlineKeyboardButton(text="Call for help", callback_data='help')],
                        [InlineKeyboardButton(text="Exit Interactive Mode", callback_data="disable_interactive")]
                   ])
    core.delLastMessage(chat_id)
    core.appendChat(bot.sendMessage(chat_id, content, reply_markup = keyboard, parse_mode="markdown"))

def sendCoreFunctKeyboard(chat_id):
    # Ok what this function does is that its will send a list
    # of command that are like really not nessesary to edit but 
    # crucial to the system. Like resetting json files, and junk
    if (not core.checkAuthlist(chat_id, "core_admin")):
        bot.sendMessage(chat_id, "You are not authorised to access this function. Contact a high level admin to gain access to this function.")
        SendCommandMain(chat_id, "Null")
        exit()
   
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="Add admin", callback_data="admin_add"),
                        InlineKeyboardButton(text="Remove admin", callback_data="admin_remove")],
                        [InlineKeyboardButton(text="Add high admin", callback_data="h_admin_add"),
                        InlineKeyboardButton(text="Remove high admin", callback_data="h_admin_remove")],
                        [InlineKeyboardButton(text="Reset core json files", callback_data="reset_json")],
                        [InlineKeyboardButton(text="☠️   Shutdown system   ☠️", callback_data="shutdown_core")],
                        [InlineKeyboardButton(text="Go back", callback_data="EnterInteractiveMode")]
                    ])
    core.delLastMessage(chat_id)
    core.appendChat(bot.sendMessage(chat_id, "*Core functions (Dangerous): * \nPlease select a command to continue :", reply_markup=keyboard, parse_mode="markdown"))

def Cancel_SendSessionList(chat_id, DayName):
    # send a list of keyboard button containing
    # all the session of a day that is specified
    # as an argument...
    session_count = parsedata.getSessionCount(chat_id, DayName)
    cancelled_session_list = parsedata.getCancelledSessionsByDay(DayName)

    if (session_count != 0 and len(cancelled_session_list) != session_count):
        keyboard = []
        print(cancelled_session_list)
        for sessionid in range(0,session_count):
            if (str(sessionid) not in cancelled_session_list): # check if this session is already cancelled
                # run this loop for each session
                # the loop runs from 0 to session_count
                # parse a the details of the sessions
                # so the data can be parsed into a keyboard
                data = parsedata.parseSessionData(chat_id,sessionid, DayName.lower())
                session_name    = data[0]
                session_start   = data[1]
                session_end     = data[2]
                lecturer        = data[4]
                venue           = data[5]
                
                keyboard_text = session_name + " | From " + str(session_start) + " to " + str(session_end) + " | " + lecturer + " | " + venue
                callback_text = "cancel_sessionbyid " + " " + str(DayName.lower()) + " " + str(sessionid)  # create a command callback system
                keyboard.append([InlineKeyboardButton(text=keyboard_text, callback_data=callback_text)])  # append the keyboard button into the keyboard
                # Make the send the keyboard


        keyboard.append([InlineKeyboardButton(text="Go Back", callback_data='cancel_session')])
        SendCustomKeyboard(chat_id, "*Cancel Session : * \nPlease select a session from the list below to cancel it : ", keyboard)
        # add the cancel button
    else:
        # if there are no session say that
        # there are no sessions in the the content
        # of the keyboard
        keyboard = []
        keyboard.append([InlineKeyboardButton(text="Go Back", callback_data='cancel_session')])
        SendCustomKeyboard(chat_id, "*Cancel Session : * \nYou have no sessions on the selected day. Revert any cancelled sessions to view them here : ", keyboard)
       
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
        [InlineKeyboardButton(text="Cancel", callback_data='EnterInteractiveMode')],
    ]
    SendCustomKeyboard(chat_id, "*Cancel Session :* \nSelect a day :", keyboardList)

def CancelSessionById(chat_id, DayName, session_id):
    # function to send modify the session list
    # so that the session will be cancelled...
    bot.sendMessage(chat_id, "*Status Return : * \n" + str(DayName).capitalize() + "'s session ID " + session_id + " has been cancelled. A blast out will be sent out in a few minutes.", parse_mode="markdown")
    SendCommandMain(chat_id, "Null Data")
    append_raw_data["cancelled"][DayName].append(session_id)
    with open('appended_sessions_list.json', 'w') as outfile: # save the file
        json.dump(append_raw_data, outfile)

def SendCancelledSessionList(chat_id):
    # function to send a list of cancelled sessions so
    # that the effects of the cancellation will be reverted...
    keyboardButtons = []
    dayList = ("monday","tuesday","wednesday","thursday","friday","saturday","sunday")
    for dayIndex in range(0, 6):
        testDay = dayList[dayIndex]
        if (len(append_raw_data["cancelled"][testDay]) != 0):
            for testSession in append_raw_data["cancelled"][testDay]:
                dayData = parsedata.parseSessionData(chat_id, int(testSession), dayList[dayIndex])
                buttonText = dayList[dayIndex].capitalize() + " | " + dayData[0] + " | " + dayData[1] + " - " + dayData[2] + " | " + dayData[5]
                callbackData = "revert_cancellation " + dayList[dayIndex] + " " + str(testSession)
                keyboardButtons.append([InlineKeyboardButton(text=buttonText, callback_data=callbackData)])
    if (len(keyboardButtons) == 0):
        # if there are no session available
        # just send a keyboard content saying so...
        keyboardButtons.append([InlineKeyboardButton(text="Go Back", callback_data='EnterInteractiveMode')])
        SendCustomKeyboard(chat_id, "*Revert Cancellation : * \nYou have no sessions cancelled. Please cancel a session so you can revert the cancellation :", keyboardButtons)
    else:
        # or else send a keyboard that lists all the sessions...
        keyboardButtons.append([InlineKeyboardButton(text="Cancel", callback_data='EnterInteractiveMode')])
        SendCustomKeyboard(chat_id, "*Revert Cancellation : * \nPlease select a session to revert its cancellation :", keyboardButtons)

def SendAppendedSessionList(chat_id):
    # function to send a list of cancelled sessions so
    # that the effects of the cancellation will be reverted...
    keyboardButtons = []
    dayList = ("monday","tuesday","wednesday","thursday","friday","saturday","sunday")
    for dayIndex in range(0, 6):
        testDay = dayList[dayIndex]
        if (len(append_raw_data["appended"][testDay]) != 0):
            for testSession in append_raw_data["appended"][testDay]:
                dayData = parsedata.parseSessionData(chat_id, int(testSession), dayList[dayIndex])
                buttonText = dayList[dayIndex].capitalize() + " | " + dayData[0] + " | " + dayData[1] + " - " + dayData[2] + " | " + dayData[5]
                callbackData = "revert_append " + dayList[dayIndex] + " " + str(testSession)
                keyboardButtons.append([InlineKeyboardButton(text=buttonText, callback_data=callbackData)])
    if (len(keyboardButtons) == 0):
        # if there are no session available
        # just send a keyboard content saying so...
        keyboardButtons.append([InlineKeyboardButton(text="Go Back", callback_data='EnterInteractiveMode')])
        SendCustomKeyboard(chat_id, "*Revert Append : * \nYou have no sessions appended. Please append a session so you can delete it, just like how my creator created me and will abandon me... :", keyboardButtons)
    else:
        # or else send a keyboard that lists all the sessions...
        keyboardButtons.append([InlineKeyboardButton(text="Cancel", callback_data='EnterInteractiveMode')])
        SendCustomKeyboard(chat_id, "*Revert Append : * \nPlease select an appended session to cancel it :", keyboardButtons)


def RevertCancellationById(chat_id, query_id, day, session_id):
    # Revert the cancellation of a session
    # via the day and session_id
    objectIndex = append_raw_data["cancelled"][day.lower()].index(str(session_id))
    del append_raw_data["cancelled"][day.lower()][objectIndex]
    with open('appended_sessions_list.json', 'w') as outfile: # save the file
        json.dump(append_raw_data, outfile)
    SendCancelledSessionList(chat_id)

def SendCustomKeyboard(chat_id, content, commands, log = True):
    # send a custom keyboard with custom commands
    # the commands will have to be sent as an array...
    keyboard = InlineKeyboardMarkup(inline_keyboard=commands)
    if (log):
        core.delLastMessage(chat_id)
        core.appendChat(bot.sendMessage( chat_id, content, reply_markup=keyboard, parse_mode="markdown"))
    else:
        bot.sendMessage(chat_id, content, reply_markup=keyboard, parse_mode="markdown")


