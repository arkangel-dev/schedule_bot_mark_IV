import aiml
import normie_functions as normie

kernel = aiml.Kernel()
kernel.learn("aiml_datasets/basics.xml")

def getRespose(query):
    return(kernel.respond(query))

def match_functions(query, chat_id):
    response = getRespose(query)
    
    if response == "MISMATCH":
        print("[-] Failed to match pattern")

    elif response == "SEND_TODAY":
        normie.sendTodaySessionList(chat_id)

    elif response == "GET_HELP":
        normie.normie_help_list(chat_id)