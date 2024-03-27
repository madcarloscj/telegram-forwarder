# Import the library
from telethon import TelegramClient, events

# Import the errors module from telethon
from telethon import errors

# Import the time module
import time

#Import the logging module
import logging

# Log the information in a logger called "copyFull"
logger = logging.getLogger('copyFull')
logger.setLevel(logging.DEBUG)

# Log the information in a file with name "copyFull.log"
fh = logging.FileHandler('copyFull.log')
fh.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
logger.addHandler(fh)

# Define your API ID and hash
API_ID = {YOUR_API_ID}
API_HASH = {YOUR_API_HASH}

# Create a client object with a new session name
client = TelegramClient('copySession', API_ID, API_HASH)

# Define the name of the groups
GROUP_SOURCE = {NAME_OF_YOUR_SOURCE_GROUP}
GROUP_DESTINATION = {NAME_OF_YOUR_DESTINATION_GROUP}

# Define an async function to get the forward the messages from the source group to the destination group
async def copy_group_to_group ():
  
	# Connect the client to the Telegram server
	await client.connect ()
  
  # Check if the client is connected
  if not client.is_connected ():
    
    # If not, raise an exception
    raise ConnectionError ('Cannot connect to the Telegram server')
  
  # Sign in the client with your phone number and verification code
  await client.start ()
  
  # Get a list of all the dialogs you have access to
  dialogs = await client.get_dialogs ()
  
  # Find the entities that matches the source group and the destination group you want
  entity1 = None
  entity2 = None
  for dialog in dialogs:
    #if dialog.id == GROUP_1:
    if dialog.name.startswith(GROUP_SOURCE):
      entity1 = dialog.entity
    if dialog.name.startswith(GROUP_DESTINATION):
      entity2 = dialog.entity

  # Check if the entity was found
  if entity1 is None:
    
    # If not, raise an exception
    raise ValueError ('Cannot find any entity corresponding to ' + GROUP_1)
    
  if entity2 is None:
    
    # If not, raise an exception
    raise ValueError ('Cannot find any entity corresponding to ' + GROUP_2)

	# Open the file in read mode
	# This file stores the last offset so that next time that you execute the code
	# the application continues from that offset id
	try:
		with open(GROUP_DESTINATION+"_offset.log", 'r') as file:
			# Read the contents of the file
			offset_str = file.read()
	except (FileNotFoundError, ValueError):
  	with open(GROUP_DESTINATION+"_offset.log", 'w') as file:
    	file.write('1')
    	offset_str = "1"

  # Convert the offset back to an integer
  offset_id = int(offset_str)
  limit = 100 # Number of messages to fetch per batch
  count = 0 # Count of messages copied

	try:
      # Get an initial of messages from the source chat
      batch = await client.get_messages(entity1, limit=limit, offset_id=offset_id, reverse=True)
    except errors.FloodWaitError as e:
			# Catch the FloodWaitError
			print(f'A wait of {e.seconds} seconds is required')
			# Sleep for the required time
			time.sleep(e.seconds)
			batch = await client.get_messages(entity1, limit=limit, offset_id=offset_id, reverse=True)

	# Keep getting batches until there are no more messages left in the source group
	while batch:
			for message in batch:
					count += 1
					print("Sending message: " + str(message.id))
					try:
							await client.send_message(entity2, message)
							offset_id = message.id
							logger.debug(str(message.id))
					except errors.FloodWaitError as e:
							# Catch the FloodWaitError
							print(f'A wait of {e.seconds} seconds is required')
							# Sleep for the required time
							time.sleep(e.seconds)
							print(f'The wait is now finished')
			try:
					# Get a new batch of messages from the source chat
					batch = await client.get_messages(entity1, limit=limit, offset_id=offset_id, reverse=True)
			except errors.FloodWaitError as e:
					# Catch the FloodWaitError
					print(f'A wait of {e.seconds} seconds is required')
					# Sleep for the required time
					time.sleep(e.seconds)
					print(f'The wait is now finished so we can retry to get the message')
					batch = await client.get_messages(entity1, limit=limit, offset_id=offset_id, reverse=True)
			if not batch:
					print("Total count: " + str(count))
					print("Offset id: " + str(offset_id))
					
					# Open a file in write mode ('w') which will truncate the file
					with open(GROUP_DESTINATION+"_offset.log", 'w') as file:
							# Write the number to the file
							file.write(str(offset_id))
					sys.exit()
			else:
					print("Finished")

# Run the async function using asyncio
import asyncio
try:
  # Try to run the function
  asyncio.run (copy_group_to_group ())
  sys.exit()
except (ConnectionError, ValueError) as e:
  # Handle the errors
  print (e)
  sys.exit()




