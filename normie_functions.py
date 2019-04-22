# normie functions
import telepot
import env
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import admin_func_lib as admin_lib

bot = telepot.Bot(env.TELEGRAM_BOT_API_KEY)

def registerUser(chat_id, context, content):
    if (context == 0):
        bot.sendMessage(chat_id, "Starting registration")
        keyboardList = [[InlineKeyboardButton(text="Click", callback_data='/register Pybrr Hon')]]
        admin_lib.SendCustomKeyboard(chat_id, "Null", keyboardList, False)
    elif (context == 1):
        bot.sendMessage(chat_id, "Part 2")
    elif (context == 2):
        bot.sendMessage(chat_id, "Part 3")
