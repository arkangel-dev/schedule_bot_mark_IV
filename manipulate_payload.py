import time
import sys
import json
import core_functions as core

# @todo Clean up manipulate_payload.py
# @body The payload file is bare bones for the system to work.; Needs more work

payload_raw = sys.argv[1]
payload = json.loads(payload_raw)
chat_id = payload["chatId"]
content = payload["content"]

status_data = core.openJsonFile("user_status_data.json")

if (str(chat_id) in status_data["awaiting_response_users"]):
    payload.update({"awaiting_data" : True })
else:
    payload.update({"awaiting_data" : False })

print(json.dumps(payload))