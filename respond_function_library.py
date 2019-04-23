import core_functions as core
import telepot
import env
import admin_func_lib as admin_lib
import time

bot = telepot.Bot(env.TELEGRAM_BOT_API_KEY)

# There function will be needed 
# to read and write to the user status data file
# Cool? Okay, Cool!

def appendStatus_await(userid, callback_function):
    # Ok so what we need to do is open a file,
    # get the data from the function's parameter
    # and then use it append an entry into the user
    # status file dictionary and save it... 
    # easy!
    user_status_data = core.openJsonFile("user_status_data.json") # ok the file is open.
    # now we append the user id as a string to the dictionary
    user_status_data["awaiting_response_users"].update({ str(userid) : { "callback_function" : callback_function }})
    core.saveJsonFile(user_status_data, "user_status_data.json")

def deleteStatus_await(userid, mainAndExit=True):
    user_status_data = core.openJsonFile("user_status_data.json") # CopyCat ;)
    # We got he other one working... now we fix the other
    if (str(userid) in user_status_data["awaiting_response_users"]):
        del user_status_data["awaiting_response_users"][str(userid)]
        core.saveJsonFile(user_status_data, "user_status_data.json")
        if mainAndExit:
            admin_lib.SendCommandMain(userid, "NULL")
            exit()

        

# Try not to mess with anything above this line...
# please... Just dont... You'll mess up something
# That's good. Just dont mess with good stuff...

def appendSession_enter(chat_id, content):
    # so this is the function to enter sessions
    # to the temporary library!
    # now the data struct is day,session_name,start_time,end_time,bring_laptop,lecturer_name,venue
    
    if (content == "/done"):
        deleteStatus_await(chat_id)
        bot.sendMessage(chat_id, "Ok, the session have been appeneded")
        admin_lib.SendCommandMain(chat_id, "Null")
        time.sleep(3)
        exit()
    
    content_count = len(content.split(","))
    if (content_count != 7):
        bot.sendMessage(chat_id, "The inputs you gave were insufficient. 7 inputs expected, " + str(content_count) + " inputs were recieved.")
    else:
        fixed_charset = []
        for x in content.split(","):
            first_char = x[0]
            if (first_char != " "):
                fixed_charset.append(x)
            else:
                fixed_charset.append(x[1:len(x)])
        send_data = "append " + fixed_charset[0] + "," + fixed_charset[1] + "," + fixed_charset[2] + "," + fixed_charset[3] + "," + fixed_charset[4] + "," + fixed_charset[5] + "," + fixed_charset[6]  
        admin_lib.append_session(chat_id, send_data)
        bot.sendMessage(chat_id, "Good job. If you have more sessions to append, keep sending them. If not send /done to finish up")

def admin_add(chat_id, content):
    if (core.lookUpUser(content)):
        core.delLastMessage(chat_id)
        bot.sendMessage(chat_id, "User @" + content + " found. Please wait.")
        deleteStatus_await(chat_id, False)
        admin_lib.admin_add(chat_id, core.lookUpUser(content, True))
    else:
        bot.sendMessage(chat_id, "User @" + content + " not found. Make sure that this user has started a chat with me prior to attempting adding him as an admin.")

    