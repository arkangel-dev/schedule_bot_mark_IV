import aiml
import normie_functions as normie
import core_functions as core

with core.suppress_stdout():
    # supress the output because I really dont
    # like the output it creates everytime a 
    # query is sent to the bot...
    kernel = aiml.Kernel()
    kernel.learn("aiml_datasets/basics.xml")
    kernel.learn("aiml_datasets/expressions.xml")
    kernel.learn("aiml_datasets/passive_agressive_personality.xml")

def getRespose(query):
    return(kernel.respond(query))

def match_functions(query, chat_id):
    response = getRespose(query)
    command = response.split()[0]
    
    if command == "MISMATCH":
        normie.sendWut(chat_id)

    elif command == "SEND_TODAY":
        normie.sendTodaySessionList(chat_id)

    elif command == "GET_HELP":
        normie.normie_help_list(chat_id)

    elif command == "DISABLE_REMINDER":
        normie.reminderToggle(chat_id, False)

    elif command == "FORWARD_CONTENT":
        normie.forwardMessage(chat_id, response.split("(_SPLITTER_)")[1])