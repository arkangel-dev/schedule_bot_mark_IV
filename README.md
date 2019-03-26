# Schedule Bot Mark IV

There will be only a single bot controlling this entire project. The bot will recieve commands from the end user such as `/today`. The bot will
also have a command that will not be listed in the command line interface. and that command is `/admin`. If used without any paramenters the
bot will start using the inline keyboad to interact with the user. This will be useful for when the admin is not comfortable with manually entering
commands.

## Using the bot

### Interactive Mode

When the admin starts using the `/admin` function without any parameters the interactive mode is started. When the buttons of the keyboard redirect user to another keyboard or message the current keyboard will delete itself before or after executing its designated task. Hence the suicide keyboards. You can disable the interactive mode by clicking on the button that says disable interactive mode or send the command `/admin disable_interactive`. This will disable the suicide keyboards and you'll have to use manual command like commands. To bring back interactive mode just send `/admin` again. 

There are some functions that interactive mode cannot work with ( for now ). And those functions include all functions that require additional parameters that the bot cannot predict. Such as appending sessions and blasting out messages. Other functions such as cancel sessions, which the bot can suggest options via the keyboard.
 
---

## Configuring Long Term Sessions
To make long term changes. The `session_list.json` file'd be modifed. The session file below is a blank template. You can any amount of sessions to each day.
```json { 
"days" :
	{ 
		"sunday" :  {
			"sessions" : []
		},
		"monday" :  {
			"sessions" : []
		},
		"tuesday" : {
			"sessions" : []
		},
		"wednesday" : {
			"sessions" : []
		},
		"thursday" :  {
			"sessions" : []
		},
		"friday" : {
			"sessions" : []
		},
		"saturday" : {
			"sessions" : []
		}
	}
}
```
To add a session append the following code to the `sessions` array of the session's respective day :
```json
["SESSION_NAME", "STARTING_TIME", "ENDING_TIME", "BRING_LAPTOP_BOOLEAN", "LECTURER_NAME", "VENUE"]
```

For example, an OOSD session to monday at 1800 hours to 1900 hours will look like this :
```json { 
"days" :
	{ 
		"sunday" :  {
			"sessions" : []
		},
		"monday" :  {
			"sessions" : []
		},
		"tuesday" : {
			"sessions" : []
		},
		"wednesday" : {
			"sessions" : []
		},
		"thursday" :  {
			"sessions" : []
		},
		"friday" : {
			"sessions" : []
		},
		"saturday" : {
			"sessions" : ["OOSD", "1800", "1900", "True", "Mr.Potatoe", "Lab 1"]
		}
	}
}
```
### Note

The start and end time have to be in 24-hour format. Or else it will mess up the arthimetic functions in the code. If you want the time in 12-hour format, convert the 24-hour format to 12-hour format <u><b>AFTER</b></u> the arthimetic functions in `parse_natural_language.py`. Use the following block of code to convert 24-hour format to 12-hour format:

```python
from datetime import datetime
# make sure the 12-hour format is a datetime object and not a string
d = datetime.strptime("10:30", "%H:%M")
d.strftime("%I:%M %p")
d = datetime.strptime("22:30", "%H:%M")
d.strftime("%I:%M %p")
```


 
---

## Appending and Cancelling sessions
To make short term modifications to the sesssions you'd have to update the `appended_session_list.json` file. The `appended_session_list.json` file will be reset at the end of every week. To check if sessions are cancelled aligned array checking is used. 

for example : when the `appended_session_list` is set to the following : 
```json
{
	"cancelled" : {
		"sunday" : [],
		"monday" : [],
		"tuesday" : [],
		"wednesday" : [],
		"thursday" : [],
		"friday" : [],
		"saturaday" : []
	},
	"appended" : {
		"sunday" : [],
		"monday" : [],
		"tuesday" : [],
		"wednesday" : [],
		"thursday" : [],
		"friday" : [],
		"saturaday" : []
	}
}

```
the output will be the following
``` ['You have 2 session(s) today. They are the following : ', 'You have OOSD from 1800 hours to 2000 hours with Nihaadh. Class will be held at Lab 1.', 'You have CNS from 2000 hours to 2200 hours with Megnha. Class will be held at NW207.', "You won't be needing your laptop"]```

and the following `appended_session_list` will give the following output:

```json {
	"cancelled" : {
		"sunday" : [],
		"monday" : [],
		"tuesday" : [],
		"wednesday" : [],
		"thursday" : [],
		"friday" : [],
		"saturaday" : []
	},
	"appended" : {
		"sunday" : [],
		"monday" : [],
		"tuesday" : [],
		"wednesday" : [],
		"thursday" : [],
		"friday" : [["OOSD", "1800", "2000", "True", "Java", "Lab1", "False"]],
		"saturaday" : []
	}
}

```
```['You have 1 session(s) today. They are the following : ', 'Your OOSD session have been cancelled', 'You have CNS from 2000 hours to 2200 hours with Megnha. Class will be held at NW207.', 'In addition to your regular classes you also have the following appended class(es) :', 'OOSD from 1800 hours to 2000 hours with Java, at Lab1.', "You won't be needing your laptop"```

---

### Note
All of the above examples are made with the `appended_session_list.json` set to the following configuration:

```json { 
"days" :
	{ 
		"sunday" :  {
			"sessions" : [
				["CNS","2000","2200","True","Mr.Krishnamoorthy","Computer Lab 2","True"]
			]
		},
		"monday" :  {
			"sessions" : []
		},
		"tuesday" : {
			"sessions" : ["Introduction to Artificial Intelligence", "1800", "2100", "Computer Lab 2", "False"]
		},
		"wednesday" : {
			"sessions" : ["OOSD" , "1900", "2200", "Computer Lab 2", "False"]
		},
		"thursday" :  {
			"sessions" : [
				["CNS", "1800", "1900", "False", "Megnha", "NW207", "False"],
				["OOSD", "1800", "2000", "True", "Nihaadh", "Lab 1", "False"]
			]
		},
		"friday" : {
			"sessions" : [
				["CNS", "1800", "1900", "False", "Megnha", "NW207", "False"],
				["OOSD", "1800", "2000", "True", "Nihaadh", "Lab 1", "False"]
			]
		},
		"saturday" : {
			"sessions" : []
		}
	}
}
```

## Additional Notes
When using to send message use the `parse_natural_language.py` file like the following:
```python
import parse_natural_language as parse_nl
print(parse_nl.getFullTodayNL())
```
