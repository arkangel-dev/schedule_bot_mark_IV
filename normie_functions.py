# normie functions
import telepot
import env
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import admin_func_lib as admin_lib
import core_functions as core

bot = telepot.Bot(env.TELEGRAM_BOT_API_KEY)

def registerUser(chat_id, content):
    #
    # Arkangel's Method to get a conditional layed string from multiple keyboards from a single function.
    # Or A.M.G.C.C.F.M.K.S.F for short. This method can be used to make a choice based avventure
    # game on telegram or something... >:D
    #
    enteredKeys = len(content.split(",")) - 1
    programmes_list = core.openJsonFile("programmes.json")

    if (enteredKeys == 0):
        # how this check system works is interesting
        # when the first check is executed the input (content)
        # will be register
        #
        # so when the code len(content.split(",")) - 1
        # is executed the result will be 0.
        #
        # Now the callback of the buttons will be register ,{year}
        # note how there is a space between the command and the word
        # register, but not between the word the comma and the year.
        # this is so it wont mess the check that executes this block
        # of code by identifying the word register, in the same time, so
        # when the split function is used on it there wont be any excess white
        # space on before the year.
        keyboardList = []
        for x in programmes_list["listings"]:
            #
            # loop rought all the properties at the beggining of
            # file. Which are the years. And make a keyboard from that
            # with the text as the property name and the callback data as register ,{propety name}
            # 
            keyboardList.append([InlineKeyboardButton(text=x, callback_data='register ,' + x)])
        keyboardList.append([InlineKeyboardButton(text="Cancel", callback_data='WIP')])

        admin_lib.SendCustomKeyboard(chat_id, "*Registration : * \nSelect an year : ", keyboardList)

    elif (enteredKeys == 1):
        # so when the first if check is done the operator len(content.split(",")) - 1
        # will give the result in 1 because the input is "register ,2019". So splitting it
        # by the command will result in the following array
        #
        # ["Register ", "2019"]
        #
        # now the len() operator will give the result 2 so lets subtract 1 from it. This is
        # not sessary but I'd prefer if it started counting from zero
        #
        keyboardList = []
        #
        # now that we have gone trought the first check we can get the user's input from the
        # callback data from the last input. This can be done by splitting the callback from the
        # button with a comma as a paramter. This will result in the followng array.
        # 
        # ["register ", "{year}"]
        # 
        # so we can get that by setting the index to one.
        #
        year = content.split(",")[1]
        #
        # Ok now we loop trought all the properties in the year property. That way we can get 
        # programme list so we can make a keyboard.
        #
        for x in programmes_list["listings"][year]:
            keyboardList.append([InlineKeyboardButton(text=x, callback_data='register ,' + year + "," + x)])
        keyboardList.append([InlineKeyboardButton(text="Go back to select an year", callback_data='register')])
        admin_lib.SendCustomKeyboard(chat_id, "*Registration : * \nSelect a programme : ", keyboardList)

    elif (enteredKeys == 2):
        #
        # ok so this is the block of
        # code that will enter the intake month
        #
        keyboardList = []
        year = content.split(",")[1]
        programme = content.split(",")[2]
        for x in programmes_list["listings"][year][programme]:
            keyboardList.append([InlineKeyboardButton(text=x, callback_data='register ,' + year + "," + programme + "," + x)])
        keyboardList.append([InlineKeyboardButton(text="Go back to select a programme", callback_data='register ,' + year)])
        admin_lib.SendCustomKeyboard(chat_id, "*Registration : * \nSelect an intake month : ", keyboardList)

    elif (enteredKeys == 3):
        #
        # So if all 3 inputs are entered, this will be executed becuase the split(',')
        # will give the result ["register ", "2019", "BSC (Hons) Computer Science", "January"]
        # subtracting 1 from the length of the array will give the result 3. So that's how we know
        # We have 3 inputs.
        #
        year = content.split(",")[1]
        programme = content.split(",")[2]
        intake = content.split(",")[3]
        #
        # delete the messeages
        #
        core.delLastMessage(chat_id)
        bot.sendMessage(chat_id, "*Registration : * \nRegistering you under *" + year + "* - *" + programme + "* - *" + intake + "* intake", parse_mode="markdown")
        #
        # update the subscription file...
        #
        subscribe_file = core.openJsonFile("subscriptions.json")
        subscribe_file["subscriptions"].update({str(chat_id) : [intake, programme, year]})
        core.saveJsonFile(subscribe_file, "subscriptions.json")