# telegram-forwarder
A tool to forward messages from one group to another using Telegram API and telethon library for python

# How to execute
Modify the telegram-forwarder.py file with your API ID and API HASH as well as the name of the source and destination groups
<p>Execute using python</p>
<code>python telegram-forwarder.py</code>

# External Files
Two files are automatically created with the execution:
- copyFull.log: with the log of the execution
- {GROUP_DESTINATION}+"_offset.log": the offset id of the last sent message. This file will help in case the process is stopped or after is resumed. Whenever new messages are available and the process is retriggered, the copy will start on the offset_id stored in this file
