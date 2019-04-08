import sys
import json
import core_functions as core


# raw = sys.argv[1]
# converted = json.loads(raw)
# chat_id = converted["chatId"]
# content = converted["content"]
# if (content.split()[0] == "/admin"):
#     exit()


user_status_data = core.openJsonFile("user_status_data.json")
awaiting_response_list = user_status_data["awaiting_response_users"]



print(len(awaiting_response_list))