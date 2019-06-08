# - *- coding: utf- 8 - *- 
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
import respond_function_library as respond_lib
import security as sec


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


# ["SESSION_NAME", "STARTING_TIME", "ENDING_TIME", "BRING_LAPTOP_BOOLEAN", "LECTURER_NAME", "VENUE"]
# ATHFAN'S CODE
# =========================================================================
# import telepot
# from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

# keyboard = InlineKeyboardMarkup(inline_keyboard=[
#                    [InlineKeyboardButton(text="hey", callback_data='/command1')],
#                    [InlineKeyboardButton(text="hey", callback_data='/command1')],
#                    [InlineKeyboardButton(text="hey", callback_data='/command1')]
#                ])

# bot = telepot.Bot("641334893:AAF1_MJ2ou9nGt4MIbAYSIWMUxfKPDCpDAw")
# bot.sendMessage(488976797, "Hello", reply_markup = keyboard)
# ===========================================================================


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
    raw_chat_data = bot.getChat(chat_id)
    username = raw_chat_data["first_name"]

    authority_list = core.openJsonFile("auth_list.json")

    
    if not (str(chat_id) in authority_list["admin"]):
        authority_string = "\nYou have complete control over *everything*"
    else:
        auth_year = authority_list["admin"][str(chat_id)][0]
        auth_programme = authority_list["admin"][str(chat_id)][1]
        auth_intake = authority_list["admin"][str(chat_id)][2]
        authority_string = "\nYou have complete control over the *" + auth_intake + "* intake of *" + auth_programme + "* of the year *" + auth_year + "*"
    

    content = "*Admin Main Menu : * \nHello " + username + ", Please select a command to continue :" + authority_string
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
                        InlineKeyboardButton(text="Remove admin", callback_data="admin_revoke")],
                        [InlineKeyboardButton(text="Add high admin", callback_data="h_admin_add"),
                        InlineKeyboardButton(text="Remove high admin", callback_data="h_admin_revoke")],
                        [InlineKeyboardButton(text="Update OTP code", callback_data="update_otp")],
                        # [InlineKeyboardButton(text="Reset core json files", callback_data="reset_json")],
                        # removed ^ these because ice bear doesn't approve
                        [InlineKeyboardButton(text="Go back", callback_data="EnterInteractiveMode")]
                    ])
    core.delLastMessage(chat_id)
    core.appendChat(bot.sendMessage(chat_id, "*Core functions : * \nPlease select a command to continue :", reply_markup=keyboard, parse_mode="markdown"))

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
    #
    # send the day list so that the user can
    # choose a day and recieve a session list
    #
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
    #
    # function to send modify the session list
    # so that the session will be cancelled...
    #
    bot.sendMessage(chat_id, "*Status Return : * \n" + str(DayName).capitalize() + "'s session ID " + session_id + " has been cancelled. A blast out will be sent out in a few minutes.", parse_mode="markdown")
    SendCommandMain(chat_id, "Null Data")
    append_raw_data["cancelled"][DayName].append(session_id)
    with open('appended_sessions_list.json', 'w') as outfile: # save the file
        json.dump(append_raw_data, outfile)

def SendCancelledSessionList(chat_id):
    #
    # function to send a list of cancelled sessions so
    # that the effects of the cancellation will be reverted...
    #
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
        #
        # if there are no session available
        # just send a keyboard content saying so...
        #
        keyboardButtons.append([InlineKeyboardButton(text="Go Back", callback_data='EnterInteractiveMode')])
        SendCustomKeyboard(chat_id, "*Revert Cancellation : * \nYou have no sessions cancelled. Please cancel a session so you can revert the cancellation :", keyboardButtons)
    else:
        # or else send a keyboard that lists all the sessions...
        keyboardButtons.append([InlineKeyboardButton(text="Cancel", callback_data='EnterInteractiveMode')])
        SendCustomKeyboard(chat_id, "*Revert Cancellation : * \nPlease select a session to revert its cancellation :", keyboardButtons)

def SendAppendedSessionList(chat_id):
    #
    # function to send a list of cancelled sessions so
    # that the effects of the cancellation will be reverted...
    #
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
        #
        # if there are no session available
        # just send a keyboard content saying so...
        #
        keyboardButtons.append([InlineKeyboardButton(text="Go Back", callback_data='EnterInteractiveMode')])
        SendCustomKeyboard(chat_id, "*Revert Append : * \nYou have no sessions appended. Please append a session so you can delete it, just like how my creator created me and will abandon me... :", keyboardButtons)
    else:
        # or else send a keyboard that lists all the sessions...
        keyboardButtons.append([InlineKeyboardButton(text="Cancel", callback_data='EnterInteractiveMode')])
        SendCustomKeyboard(chat_id, "*Revert Append : * \nPlease select an appended session to cancel it :", keyboardButtons)


def RevertCancellationById(chat_id, query_id, day, session_id):
    #
    # Revert the cancellation of a session
    # via the day and session_id
    #
    objectIndex = append_raw_data["cancelled"][day.lower()].index(str(session_id))
    del append_raw_data["cancelled"][day.lower()][objectIndex]
    with open('appended_sessions_list.json', 'w') as outfile: # save the file
        json.dump(append_raw_data, outfile)
    SendCancelledSessionList(chat_id)

def SendCustomKeyboard(chat_id, content, commands, log = True):
    #
    # send a custom keyboard with custom commands
    # the commands will have to be sent as an array...
    #
    keyboard = InlineKeyboardMarkup(inline_keyboard=commands)
    if (log):
        core.delLastMessage(chat_id)
        core.appendChat(bot.sendMessage( chat_id, content, reply_markup=keyboard, parse_mode="markdown"))
    else:
        bot.sendMessage(chat_id, content, reply_markup=keyboard, parse_mode="markdown")

def admin_add(chat_id, context):
    #
    # all right lets go over how this function works before
    # I forget how it works because it seems I only know how
    # it works when Im high on a sugar rush and Im out of
    # Munchy cookies.
    #
    # So this function keeps track of which which stage its on
    # is by counting the number of objects the variable 'context'
    # contain (yes context is a bad name for the varaible but whatever)
    # 
    # Soou the first time the function is executed the context will be
    # plain command. When the function 'len(context.split(",")) - 1 is used
    # it'll spit out the number of useful data the context variable is containing
    # . the function splits the context variable by the using the commas as a separator
    # So using commas in the Usernames, programme names is a big no no. Then we find the
    # length of it which on the first try will be 1. then we subtract 1 from it because 
    # the command is not a really useful piece of information.
    #
    content_count = len(context.split(",")) - 1
    content = context.split(",")
    programmes_list = core.openJsonFile("programmes.json")

    if (content_count == 0):
        #
        # if the content count variable is zero then it means
        # that there is not data in the context variable and
        # we should ask the user to input the data.
        # how ever this not any data input. We are requesting
        # the user to send information and lock the user in a
        # loop until s/he gives a valid input for uses an escape command
        #
        respond_lib.appendStatus_await(chat_id, "admin_add")
        core.delLastMessage(chat_id)
        core.appendChat(bot.sendMessage(chat_id, "*Add admin :* \nPlease enter the username of the user whom you wish to add as an admin.", parse_mode="markdown"))
    
    elif (content_count == 1):
        #
        # from here its pretty straight forward. The user is presented
        # with a list of buttons with is read from the programmes.json
        # file.
        #
        # then the user makes choices and every time the user clicks
        # button it will go to the next stage with the data from the
        # previous stage as an element of a list which is stored in the
        # variable 'context'
        #
        keyboardList = []
        user_id = content[1]
        for x in programmes_list["listings"]:
            keyboardList.append([InlineKeyboardButton(text=x, callback_data='admin_add ,' + user_id + "," + x)])
            #
            # please note in the above line the for loops
            # inline keyboard line has added a comma
            # between the data. this is because without the comma
            # the split(',') function will not work.
            #
        keyboardList.append([InlineKeyboardButton(text="Go back to enter username", callback_data='admin_add')])
        #
        # this additional button is here to send the user back to selecting
        # username. because of reasons...
        #
        username = core.openJsonFile("user_list.json")["users"][content[1]][0]
        if (core.checkAuthlist(content[1], "admin")):
            bot.sendMessage(chat_id, "*Add admin : * \nUser @" + username + " is already registered. Proceeding will overwrite the previous registration. If you wish to /cancel , do it. \n\nWe are now selecting which class this admin has control over. You have to specify the year, intake month and the programme.", parse_mode="markdown")
        else:
            bot.sendMessage(chat_id, "*Add admin : * \nUser @" + username + " found. We are now selecting which class this admin has control over. You have to specify the year, intake month and the programme.", parse_mode="markdown")
        
        #
        # Send this line because why the hell not ^
        #
        SendCustomKeyboard(chat_id, "*Add admin : * \nSelect the year of you enrollment : ", keyboardList)

    elif (content_count == 2):
        keyboardList = []
        #
        # ^ Init the keyboard array
        # because we have... or do we?
        #
        user_id = content[1]
        year = content[2]
        #
        # make the content from from the context
        # data. This content is put into user id and
        # year variable to streamline the process of
        # making the keyboard
        #
        for x in programmes_list["listings"][year]:
            keyboardList.append([InlineKeyboardButton(text=x, callback_data='admin_add ,' + user_id + "," + year + "," + x)])
        keyboardList.append([InlineKeyboardButton(text="Go back to select an year", callback_data='register' + ',' + user_id)])
        SendCustomKeyboard(chat_id, "*Registration : * \nSelect a programme : ", keyboardList)

    elif (content_count == 3):
        #
        # ok so this is the block of
        # code that will enter the intake month
        #
        keyboardList = []
        user_id = content[1]
        year = content[2]
        programme = content[3]
        #
        # So this stage is same as the two previous function
        # so nothing here to explain... soou yeah...
        #
        for x in programmes_list["listings"][year][programme]:
            keyboardList.append([InlineKeyboardButton(text=x, callback_data='admin_add ,' + user_id + "," + year + "," + programme + "," + x)])
        keyboardList.append([InlineKeyboardButton(text="Go back to select a programme", callback_data='admin_add,' + user_id + "," + year)])
        SendCustomKeyboard(chat_id, "*Registration : * \nSelect an intake month : ", keyboardList)

    elif (content_count == 4):
        user_id = content[1]
        year = content[2]
        programme = content[3]
        intake = content[4]
        #
        # DEV Note : The SendCustomKeyboard() function has its own core.DeleteLastMessage()
        # line. Idk why it was added there...
        #
        # bot.sendMessage(chat_id, str(user_id) + " " + year + " " + programme + " " + intake)
        core.delLastMessage(chat_id)
        bot.sendMessage(chat_id, "*Registration : * \n I am now adding the user to admin list, with the authority of full control over the class of *" + year + "* / *" + programme + "* / *" + intake + "*", parse_mode="markdown")

        raw_auth_list = core.openJsonFile("auth_list.json")
        user_32bitKey = sec.generateKey()
        raw_auth_list["admin"].update({user_id : [year, programme, intake, user_32bitKey]})
        #
        # we are now adding the the user's 32 bit key and authority data to the
        # the json file
        #
        username = bot.getChat(int(user_id))["first_name"]
        bot.sendMessage(int(user_id), u"🎉*Congratulations : *🎉 \nHello " + username + ", You have been added to my system as an administrator, with the authority of full session control over the class of *" + year + "* / *" + programme + "* / *" + intake + "*.", parse_mode="markdown")
        #
        # So now we are going to send the new admin the good news that he has been added
        # to the system as an administrator
        #
        core.saveJsonFile(raw_auth_list, "auth_list.json")
        SendCommandMain(chat_id, "Null")
    
def admin_revoke(chat_id, context):
    #
    # Now we make use the method that we used for the /admmin_add function
    # to fit the entire process in a single function. But splitting the context
    # of each stage and splitting and counting the parts...
    #
    content_count = len(context.split(",")) - 1
    content = context.split(",")

    if (content_count == 0):
        #
        # all right so the first thing we have to do is make a list
        # of usernames and their authority details. Maybe the programme name
        # and year will suffice. ( on second thought, I'll just leave it as is
        # for now and send only the usernames)
        #
        auth_admin_list = core.openJsonFile("auth_list.json")["admin"]
        #
        # first we make a list of all the chatids with them converted to
        # acutal numbers intead of strings
        #
        # but first lets check if there are admins to begin with...
        if len(auth_admin_list) == 0:
            bot.sendMessage(chat_id, "*Revoke Admin : * \nThere are no admins registered to my system. Add an admin to kick them out.", parse_mode="markdown")
            SendCommandMain(chat_id, "null")
            exit()
        # then we move on
        userlist = []
        for x in auth_admin_list:
            userlist.append(int(x))
        #
        # now that we have a list of the chat ids we can not make
        # a list of all the usernames for the keyboard...
        # We'll use the getChat() function of telepot to get that
        #
        keyboardList = []
        for x in userlist:
            username_curr = bot.getChat(x)["username"]
            keyboardList.append([InlineKeyboardButton(text="@"+username_curr, callback_data='admin_revoke ,' + str(x))])
        SendCustomKeyboard(chat_id, "*Revoke Admin : * \nSelect a username : ", keyboardList)

    elif content_count == 1:
        #
        # now we see if user has given us a user name. and if he has we will delete their
        # entry is the json file
        #
        authlist = core.openJsonFile("auth_list.json")
        del authlist["admin"][str(content[1])]
        print(authlist)
        core.saveJsonFile(authlist, "auth_list.json")
        core.delLastMessage(chat_id)
        bot.sendMessage(chat_id, "*Revoke Admin : * \nUser has been revoked of adminstrative rights.", parse_mode="markdown")
        bot.sendMessage(int(content[1]), "*Notice* \nYour adminstrative rights have been revoked. Sorry. 😞💔", parse_mode="markdown")
        #
        # send the admin who got revoked the news of him getting kicked out of the system.
        # I wonder if I can do shit like this when I get an actual job
        #
        SendCommandMain(chat_id, "null")

def h_admin_add(chat_id, context):
    #
    # so the first step is the same as when adding normal
    # midlevel admins to the system. Getting the username
    #
    # but before we can do that we have to check if the username
    # has already been provided. you following? no? cool!
    #
    content_count = len(context.split(",")) - 1
    content = context.split(",")

    if (content_count == 0):
        #
        # aaalllright.. now the first thing we have to do when getting string input from the system is
        # locking him a time loop. Dr strange style... then we bargain...
        #
        # but to be more serious we lock them is a loop that is in a separate function.
        # Then the input is verified and the user is released from the loop. or else 
        # the user will re-prompted to re-enter the data.
        # The only other way to exit this time loop is to send the trusty old /cancel command
        #
        respond_lib.appendStatus_await(chat_id, "h_admin_add")
        core.delLastMessage(chat_id)
        core.appendChat(bot.sendMessage(chat_id, "*Add core admin :* \nPlease enter the username of the user whom you wish to add as an admin. If you wish to cancel please /cancel", parse_mode="markdown"))

    elif (content_count == 1):
        #
        # all right now we have got the user we need to generate a OTP key so that 
        # this core admin will have secure access to the system
        #
        user_code = sec.generateKey()
        auth_file = core.openJsonFile("auth_list.json")
        user_id = content[1]

        otp_url = sec.generateOtpAppUrl(user_code, bot.getChat(user_id)["first_name"], "FRIDAY Schedule Bot")
        sec.generateAndSaveQrCode(otp_url, "qr_code.png")

        bot.sendMessage(int(user_id), "🎉*Congratulations :*🎉\nHello " + bot.getChat(int(user_id))["first_name"] + ", You have been added to my system as a core admin. As a core admin you have (almost) complete control over my system. Here is a QR Code with the OTP url, please scan this and store it on a secure device as you'll need it now that you're a core admin. \nYou can send /admin to activate interactive mode.", parse_mode="markdown")

        core.sendImg(int(user_id), "qr_code.png")

        auth_file["core_admin"].update({str(user_id) : [user_code]})
        core.saveJsonFile(auth_file, "auth_list.json")
        bot.sendMessage(chat_id, "I have added the user @" + bot.getChat(int(user_id))["username"] + " to the system as a core administrator")
        SendCommandMain(chat_id, "null")

def verifyOtp(chat_id, content):
    #
    # so this function is used to verify the qr code without actually doing any
    # core functions...
    #
    if not core.checkAuthlist(chat_id, "core_admin"):
        #
        # in case a normie admin finds this function and tries
        # do something they're not capable of
        #
        bot.sendMessage(chat_id, "You are not a core admin and you don't even have an OTP url. So just dont")
        SendCommandMain(chat_id, "null")
        exit()
    if len(content.split()) == 2:
        verification_code = content.split()[1]
        if (sec.verifyOtp(chat_id, verification_code)):
            bot.sendMessage(chat_id, "OTP code verification passed, Your OTP codes are still valid. 👍")
        else:
            bot.sendMessage(chat_id, "OTP code verification failed, Please update your OTP application as soon as possible. 👎")
    else:
        bot.sendMessage(chat_id, "You didnt send a test key, dumbass")
    # SendCommandMain(chat_id, "Null")

def updateOtpCodes(chat_id):
    #
    # this is the function to update the user's otp qr code because he fucking lost it!
    # 
    bot.sendMessage(chat_id, "What the fuck did you do with your old OTP qr code? Whatever here is your new OTP QR code. Dont leak it this time dumbass")
    sec.updateQrCode(chat_id)
    core.sendImg(chat_id, "qr_code.png")
    sendCoreFunctKeyboard(chat_id)
