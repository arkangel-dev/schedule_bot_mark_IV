import sys
import json

# ["SESSION_NAME", "STARTING_TIME", "ENDING_TIME", "BRING_LAPTOP_BOOLEAN", "LECTURER_NAME", "VENUE"]

raw = sys.argv[1]
converted = json.loads(raw)
chatId = converted["chatId"]
content = converted["content"]
command = content.split()[0]
arguments = (content.split()[1]).split(",")
print(command)
print(arguments)