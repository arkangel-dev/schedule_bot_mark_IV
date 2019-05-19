# this function will be looped into by the node-red server multiple times a second
# and every time the file is executed the file will read a json file that stores a time
# date, offset time and a function on it.
#
# import the classes as usual
import core_functions as core
from datetime import datetime
from datetime import timedelta
import parse_data
import env
import telepot

bot = telepot.Bot(env.TELEGRAM_BOT_API_KEY)

# load the json file
reminders_json = core.openJsonFile("reminders.json")
session_json = core.openJsonFile("session_list.json")
subscriptions = core.openJsonFile("subscriptions.json")

# first of all we need to loop through the user
# subscriptions. And just... you know... do stuff
for user in subscriptions["subscriptions"]:

    # define the subscriptiion details...
    intake = subscriptions["subscriptions"][user][0]
    programme = subscriptions["subscriptions"][user][1]
    year = subscriptions["subscriptions"][user][2]
    notifciationIsEnabled = subscriptions["subscriptions"][str(user)][3]
    offsetTime = subscriptions["subscriptions"][str(user)][4]
    latestReminder = subscriptions["subscriptions"][str(user)][4]


    # first we check if user even wants reminders
    if parse_data.parseBooleans(notifciationIsEnabled):
        print("Reminder System Is Enabled For User ID " + user) 
        # todayDay = datetime.today().strftime("%A").lower()
        todayDay = "monday"

        # loop trough all the sessions
        for sessions in session_json[year][programme][intake][todayDay]["sessions"]:
            start_time = datetime.strptime(sessions[1], '%H%M')
            session_name = sessions[0]
            latest_time_date = (start_time - timedelta(minutes = int(offsetTime)))
            latest_time = (start_time - timedelta(minutes = int(offsetTime))).time()

            # check if current time is less than the latest time and if the current time is less than the (latest time + 5 seconds)
            # that 5 seconds is synced with the node red system so that multiple message wont be sent to the user.
            if (latest_time <= datetime.now().time()) and (datetime.now().time() < (latest_time_date + timedelta(seconds = 5)).time() ):
                bot.sendMessage(int(user), "Hey man, You have your *" + session_name + "* class in *" + str(offsetTime) + "* minutes. ", parse_mode="Markdown")
                print("Message Sent!")

 