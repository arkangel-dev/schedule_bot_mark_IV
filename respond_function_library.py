import core_functions as core
import telepot
import env
import admin_func_lib as admin_lib

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

def deleteStatus_await(userid):
    user_status_data = core.openJsonFile("user_status_data.json") # CopyCat ;)
    # We got he other one working... now we fix the other
    if (str(userid) in user_status_data["awaiting_response_users"]):
        del user_status_data["awaiting_response_users"][str(userid)]
        core.saveJsonFile(user_status_data, "user_status_data.json")
        admin_lib.SendCommandMain(userid, "NULL")
        exit()

        

# Try not to mess with anything above this line...
# please... Just dont... You'll mess up something
# That's good. Just dont mess with good stuff...

def appendSession_enter(chat_id, content):
    # so this is the function to enter sessions
    # to the temporary library!
    # now the data struct is day,session_name,start_time,end_time,bring_laptop,lecturer_name,venue
    content_count = len(content.split(","))
    if (content_count != 7):
        bot.sendMessage(chat_id, "The inputs you gave were insufficient. 7 inputs expected, " + str(content_count) + " inputs were recieved.")
    else:
        bot.sendMessage(chat_id, "Input has been accepted. :)")