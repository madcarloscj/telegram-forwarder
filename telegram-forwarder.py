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
    

  # In which message you want to start
  offset_id = 1 # Initial offset value
  limit = 10 # Number of messages to fetch per batch
  count = 0 # Count of messages copied
  while True:
    try:
        # We get a batch with a {limit} number of messages starting from the offset where we are
        print("Getting new batch with offset " + str(offset_id))
        
        # Get a batch of messages from the source group
        # The reverse parameter is to get the messages from lower to higher id so that the groups are copied same as they are
        batch = await client.get_messages(entity1, limit=limit, offset_id=offset_id, reverse=True)
        
        # If the batch is empty, break the loop print the total number of messages copied and leave
        if not batch:
          print("Total count: " + str(count))
          break

        # Go through all the messages in the batch
        for message in batch:
            count += 1
            print("Sending message: " + str(message.id))

            # Send the message to the destination group
            # The message will be sent without sender, if you want to keep the sender you should use the forward_message option
            await client.send_message(entity2, message)

            # The offset should be updated with the latest message.id that was used
            offset_id = message.id
            logger.debug(str(message.id))
        
        # There is a limit on the Telegram API on the number of request and due to that a wait must be implemented
        time.sleep(30)
    except errors.FloodWaitError as e:
      # Catch the FloodWaitError
      print(f'A wait of {e.seconds} seconds is required')
      # Sleep for the required time
      time.sleep(e.seconds)

  print("Copy completed")
  logger.debug("Copy completed")

# Run the async function using asyncio
import asyncio
try:
  # Try to run the function
  asyncio.run (copy_group_to_group ())
except (ConnectionError, ValueError) as e:
  # Handle the errors
  print (e)




