# Schedule Bot Mark IV

Schedule bot Mark IV (also dubbed as FRIDAY) is the 4th version of a sheduling system integerated with the Telegram bot API platform and is the first version of the  series to work without giving the maintainer and/or the end-user an aneurysm. This version of the system has the following capabilites:

- Fetching schedules
- Multiple programmes, intakes and years
- Interpreting schedules in a natural language
- Reminding of users of schedules n minutes before a session starts
- Multiple core admins
- OTP verification for core admin functions
- Multiple admins for programmes, years and intakes
- Primitive natural language processing via AIML
- Agressive personality
- Append / Cancel sessions on the fly

## Installing the bot
### Node-Red Setup

Yes, you'll need node-red for this. Also you'll need to install the following nodes.

```
npm install node-red-contrib-chatbot
npm install node-red-contrib-python3-function
npm install node-red-contrib-pythonshell
npm install node-red-contrib-telegrambot
npm install node-red-contrib-telegrambot-home
```

Then you'll need to import the following node configuration:

```json
[{"id":"32002f64.828618","type":"tab","label":"Telegram Schedule Bot (TESTING)","disabled":false,"info":""},{"id":"bbc79e48.4ce02","type":"telegram receiver","z":"32002f64.828618","name":"","bot":"c125d188.a3af18","saveDataDir":"","x":95,"y":276,"wires":[["3229d1cf.98e61e"],[]]},{"id":"fe9550f4.fcddd8","type":"pythonshell in","z":"32002f64.828618","name":"Main Processing Function","pyfile":"O:\\GitHub\\schedule_bot_mark_IV\\test_run.py","virtualenv":"","continuous":false,"stdInData":false,"x":1423.9000244140625,"y":290,"wires":[["9183db4f.0bfd1"]]},{"id":"a2371f9.da483e","type":"catch","z":"32002f64.828618","name":"","scope":null,"uncaught":false,"x":1477.5,"y":425.6000061035156,"wires":[["9183db4f.0bfd1"]]},{"id":"261ed448.d3e5b4","type":"pythonshell in","z":"32002f64.828618","name":"Adminsitrative Functions","pyfile":"O:\\GitHub\\schedule_bot_mark_IV\\admin_functions.py","virtualenv":"","continuous":false,"stdInData":false,"x":1425.5,"y":334.4000244140625,"wires":[["9183db4f.0bfd1"]]},{"id":"4eb8821d.5788e4","type":"json","z":"32002f64.828618","name":"Convert to string","property":"payload","action":"str","pretty":false,"x":1169.5,"y":333.4000244140625,"wires":[["261ed448.d3e5b4"]]},{"id":"d7289206.60aa48","type":"telegram event","z":"32002f64.828618","name":"Keyboard_Stuff","bot":"c125d188.a3af18","event":"callback_query","autoanswer":false,"x":85,"y":384.60003662109375,"wires":[["1d39eb9e.453b14"]]},{"id":"9183db4f.0bfd1","type":"debug","z":"32002f64.828618","name":"Final Debugging","active":true,"tosidebar":true,"console":true,"tostatus":true,"complete":"payload","targetType":"msg","x":1764.5,"y":294.79998779296875,"wires":[]},{"id":"c431903f.a8749","type":"telegram command","z":"32002f64.828618","name":"/admin handler","command":"/admin","bot":"c125d188.a3af18","strict":false,"x":85,"y":329.5999755859375,"wires":[["2642cf9b.6ee4f"],[]]},{"id":"f170c9f7.41de98","type":"pythonshell in","z":"32002f64.828618","name":"Administrative Respond functions","pyfile":"O:\\GitHub\\schedule_bot_mark_IV\\admin_respond_functions.py","virtualenv":"","continuous":false,"stdInData":false,"x":1454.5,"y":248.20001220703125,"wires":[["9183db4f.0bfd1"]]},{"id":"3229d1cf.98e61e","type":"pythonshell in","z":"32002f64.828618","name":"Check if Awaiting Data","pyfile":"O:\\GitHub\\schedule_bot_mark_IV\\manipulate_payload.py","virtualenv":"","continuous":false,"stdInData":false,"x":408.5,"y":297,"wires":[["8a253e39.2bb5c8"]]},{"id":"1446f66e.7bae72","type":"switch","z":"32002f64.828618","name":"Switch if awaiting data","property":"payload.awaiting_data","propertyType":"msg","rules":[{"t":"true"},{"t":"false"}],"checkall":"true","repair":false,"outputs":2,"x":904.2000732421875,"y":274,"wires":[["1cd6bc7b.b365ac"],["3dc685ae.ecd012"]]},{"id":"2642cf9b.6ee4f","type":"pythonshell in","z":"32002f64.828618","name":"Check if Awaiting Data","pyfile":"O:\\GitHub\\schedule_bot_mark_IV\\manipulate_payload.py","virtualenv":"","continuous":false,"stdInData":false,"x":408.20001220703125,"y":337.20001220703125,"wires":[["a4199e6.6b948e"]]},{"id":"3dc685ae.ecd012","type":"json","z":"32002f64.828618","name":"Convert to string","property":"payload","action":"str","pretty":false,"x":1165,"y":291,"wires":[["fe9550f4.fcddd8"]]},{"id":"8a253e39.2bb5c8","type":"json","z":"32002f64.828618","name":"Convert to Object","property":"payload","action":"obj","pretty":false,"x":649,"y":298,"wires":[["1446f66e.7bae72"]]},{"id":"1cd6bc7b.b365ac","type":"json","z":"32002f64.828618","name":"Convert to string","property":"payload","action":"str","pretty":false,"x":1166,"y":252,"wires":[["f170c9f7.41de98"]]},{"id":"69b77233.d12264","type":"switch","z":"32002f64.828618","name":"Switch if awaiting data","property":"payload.awaiting_data","propertyType":"msg","rules":[{"t":"true"},{"t":"false"}],"checkall":"true","repair":false,"outputs":2,"x":903,"y":317,"wires":[[],["4eb8821d.5788e4"]]},{"id":"a4199e6.6b948e","type":"json","z":"32002f64.828618","name":"Convert to Object","property":"payload","action":"obj","pretty":false,"x":649.7999267578125,"y":339,"wires":[["69b77233.d12264"]]},{"id":"1d39eb9e.453b14","type":"pythonshell in","z":"32002f64.828618","name":"Check if Awaiting Data","pyfile":"O:\\GitHub\\schedule_bot_mark_IV\\manipulate_payload.py","virtualenv":"","continuous":false,"stdInData":false,"x":402.8500061035156,"y":386.8500061035156,"wires":[["52617934.eca718"]]},{"id":"52617934.eca718","type":"json","z":"32002f64.828618","name":"Convert to Object","property":"payload","action":"obj","pretty":false,"x":635.449951171875,"y":388.6499938964844,"wires":[["3d4f4d5.c5df5b2"]]},{"id":"3d4f4d5.c5df5b2","type":"switch","z":"32002f64.828618","name":"Switch if awaiting data","property":"payload.awaiting_data","propertyType":"msg","rules":[{"t":"true"},{"t":"false"}],"checkall":"true","repair":false,"outputs":2,"x":904.6500244140625,"y":370.6499938964844,"wires":[[],["10a47c3e.14d8ac"]]},{"id":"10a47c3e.14d8ac","type":"json","z":"32002f64.828618","name":"Convert to string","property":"payload","action":"str","pretty":false,"x":1169.1500244140625,"y":381.0500183105469,"wires":[["828d518d.f7ae8"]]},{"id":"828d518d.f7ae8","type":"pythonshell in","z":"32002f64.828618","name":"Keyboard Buttons","pyfile":"O:\\GitHub\\schedule_bot_mark_IV\\keyboard_stuff.py","virtualenv":"","continuous":false,"stdInData":false,"x":1408.1500244140625,"y":377.0500183105469,"wires":[["9183db4f.0bfd1"]]},{"id":"576ae91d.cd1b4","type":"comment","z":"32002f64.828618","name":"Link to python file","info":"The _\"Check if Awaiting Data\"_ nodes have to be linked to the file, _\"manipulate_keyboard.py\"_","x":388.1166687011719,"y":436.1999816894531,"wires":[]},{"id":"c125d188.a3af18","type":"telegram bot","z":"","botname":"FRIDAY","usernames":"","chatids":"","baseapiurl":"","updatemode":"polling","pollinterval":"1","usesocks":false,"sockshost":"","socksport":"6667","socksusername":"anonymous","sockspassword":"","bothost":"","localbotport":"8443","publicbotport":"8443","privatekey":"","certificate":"","useselfsignedcertificate":false,"verboselogging":false}]
```

Then you'll need to need to link the python nodes to their python files.

| Nodes | Files |
| --- | --- |
| Check if Awaiting Data | `manipulate_payload.py` |
| Administrative Respond functions | `admin_respond_functions.py`|
| Main Processing Function | `test_run.py` |
| Adminsitrative Functions | `admin_functions.py` |
| Keyboard Buttons | `keyboard_stuff.py` |

And finally you'll need the following python libraries

```
pip install telegram
pip intall telepot
pip intall pillow
pip install pyotp
pip install qrcode
pip install aiml
```

### Telegram bot commands

This is command set for the bots inline commands, send @botfather `/setcommands`.

```
today - Sends today's schedule
help - Get help
start - Starts the bot, duh
register - Register your account to a programme
admin - Start interactive mode
cancel - Cancels current operation
dontremindme - Stop sending reminders
remindme - Re-enable reminders
remindmein - Set offset for reminders
```

---

## Using the bot
### Interactive Mode

When the admin starts using the `/admin` function without any parameters the interactive mode is started. When the buttons of the keyboard redirect user to another keyboard or message the current keyboard will delete itself before or after executing its designated task. Hence the suicide keyboards. You can disable the interactive mode by clicking on the button that says disable interactive mode or send the command `/admin disable_interactive`. This will disable the suicide keyboards and you'll have to use manual command like commands. To bring back interactive mode just send `/admin` again. Like so : 

<p align="center">
<img src="documentation/admin_start.PNG">
</p>

There are some functions that interactive mode cannot work with ( for now ). And those functions include all functions that require additional parameters that the bot cannot predict. Such as appending sessions and blasting out messages. Other functions such as cancel sessions, which the bot can suggest options via the keyboard.

---

### Appending and Cancelling Session Via Interactive Mode
You can append and cancel sessions from the interactive mode. You have to click on `Manipulate Sessions`. When you do so you'll be presented with the following keyboard.

<p align="center">
	<img src="documentation/manipulate_sessions.PNG">
</p>

Now to cancel a session click on `cancel session`. From here you'll be presented with the following keyboard: 

<p align="center">
	<img src="documentation/cancel_session_day_list.PNG">
</p>

Now click on a day and you'll presented with a list of sessions available on that day. Click on a session to cancel it. You can revert the affects of a cancelled session via the `Revert Cancelled` button. Anyway here is a keyboard that will be presented to you when you choose a day : 

<p align="center">
	<img src="documentation/cancel_session_list.PNG">
</p>

---

## Additional Notes
When using to send message use the `parse_natural_language.py` file like the following:
```python
import parse_natural_language as parse_nl
print(parse_nl.getFullTodayNL())
```

---

# Changelog

## Reminder system

The bot will now remind the user of sessions N number of minutes before said session starts. The user can opt out of the reminder by sending `/dontremindme` and re-enable it by sending `/remindme`. Also the user can set the N number of minutes before session starts by sending `/remindmein N` where N represents the nummber of minutes.

## Update : Security (OTP Verification)

The bot will generate one-time-passwords only for core admins that will be prompted only when core admins attempt to add other admins or core admins to the system or other high priority functions.

## Update : Multi Level Data Processing (MLDP)
### Introduction

So this update will mess up a lot things. This because when the bot is processing information of more than one class it'll need new data stuructures to store the details of those classes. So the entire json format is re-designed will will not be compatible with the data parsing scripts and natural language files, mainly data parsing script.

## Update : Add admin function
### How it works

So it works by asking the user to send a username without the '@'. Then it will check if the entered username is in the `user_list.json` file which contains a list of all the users and their user ids. (nothing shady there >:D). So the user file is maintained by the `maniplate_payload.py` file because all the data that gets sent to the bot passes trough the node that is linked to `manipulate_payload.py` file. So this will store the user data as its secondary function. From here its just standard 'putting data in the callback data` stuff.

