# schedule_bot_mark_IV

There are two bots users in this project. One will be used to notify the users. and the other will be used the maintainers
to update and push messages from Villa College Student desk. The second bot will also be used to cancel and reschedule sessions.

To make short term modifications to the sesssions you'd have to update the `appended_session_list.json` file. To make long term changes
the `session_list.json` file'd be modifed. The `appended_session_list.json` file will be reset at the end of every week.

for example : when the `appended_session_list` is set to the following : 
```json
{
	"cancelled" : {
		"sunday" : [
		],
		"wednesday" : [
		],
		"thursday" : [
		]
	},
	"appended" : {
		"thursday" : [

		]
	}
}
```
the output will be the following
``` ['You have 2 session(s) today. They are the following : ', 'You have OOSD from 1800 hours to 2000 hours with Nihaadh. Class will be held at Lab 1.', 'You have CNS from 2000 hours to 2200 hours with Megnha. Class will be held at NW207.', "You won't be needing your laptop"]```

and the following `appended_session_list` will give the following output:

```json {
	"cancelled" : {
		"sunday" : [
		],
		"wednesday" : [
		"1",
		"2"
		],
		"thursday" : [
		"0"
		]
	},
	"appended" : {
		"thursday" : [
			[	"OOSD",
				"1800",
				"2000",
				"True",
				"Java",
				"Lab1"
			]
		]
	}
}
```
```['You have 1 session(s) today. They are the following : ', 'Your OOSD session have been cancelled', 'You have CNS from 2000 hours to 2200 hours with Megnha. Class will be held at NW207.', 'In addition to your regular classes you also have the following appended class(es) :', 'OOSD from 1800 hours to 2000 hours with Java, at Lab1.', "You won't be needing your laptop"```

and so on...

