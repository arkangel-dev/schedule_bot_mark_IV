# admin function library


def getList
    #
    # List command
    # invoked by /list
    # any additional arugemnts are ignored
    #
    session_list = []
    day_list = ("monday","tuesday","wednesday","thursday","friday","saturday","sunday")
    for x in day_list:
        session_list.append("*" + x + "* : \n")
        if len(append_raw_data["appended"][x]) != 0:
            count = 0
            for y in append_raw_data["appended"][x]:
                session_list.append("`" + str(count) + " : " + str(y) + "`\n")
                count += 1
    finalString = ""
    for x in session_list:
        finalString += x
    bot.sendMessage(chat_id, finalString, parse_mode="markdown")