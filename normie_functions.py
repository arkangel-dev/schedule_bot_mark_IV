# normie functions
import telepot
import env
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import admin_func_lib as admin_lib
import core_functions as core

bot = telepot.Bot(env.TELEGRAM_BOT_API_KEY)

def registerUser(chat_id, content):
    enteredKeys = len(content.split(",")) - 1
    programmes_list = core.openJsonFile("programmes.json")

    if (enteredKeys == 0):
        keyboardList = []
        # keyboardList = [
        #     [InlineKeyboardButton(text="2018", callback_data='/register ,2018')],
        #     [InlineKeyboardButton(text="2019", callback_data='/register ,2019')]
        # ]
        for x in programmes_list["listings"]:
            keyboardList.append([InlineKeyboardButton(text=x, callback_data='/register ,' + x)])

        admin_lib.SendCustomKeyboard(chat_id, "Select an year : ", keyboardList)

    elif (enteredKeys == 1):
        keyboardList = []
        # keyboardList = [
        #     [InlineKeyboardButton(text="Jan", callback_data='/register ' + content.split(",")[1] + " Jan")],
        #     [InlineKeyboardButton(text="Feb", callback_data='/register ' + content.split(",")[1] + " Feb")]
        # ]
        year = content.split(",")[1]
        for x in programmes_list["listings"][year]:
            keyboardList.append([InlineKeyboardButton(text=x, callback_data='/register ,' + year + "," + x)])
        admin_lib.SendCustomKeyboard(chat_id, "Select a programme : ", keyboardList)