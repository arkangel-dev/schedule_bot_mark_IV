# Schedule Bot Mark IV

There are two bots users in this project. One will be used to notify the users. and the other will be used by the maintainers
to update and push messages from Villa College Student desk, also the second bot will also be used to cancel and reschedule sessions.

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
To add a session append `json ["OOSD", "1800", "2000", "True", "Nihaadh", "Lab 1", "False"]` to the `sessions` array of the session's respective day

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
