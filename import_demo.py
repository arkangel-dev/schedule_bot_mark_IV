import json
from pprint import pprint
from datetime import datetime

with open('session_list.json') as f:
    data = json.load(f)


output = data["days"]["wednesday"]["sessions"]
print(output)


#	free_day			: 	0
#	session_name 		: 	1
#	start_time			: 	2
#	end_time			: 	3
#	bring_laptop		: 	4
#	lecturer			: 	5
#	venue				: 	6
#	other_requirements	: 	7
	
