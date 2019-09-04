"""

Lydia AI plugin for userbot.

Description: A module that Act as a chatbot and chat with a User/other Bot.

 			This Module Needs CoffeeHouse API to work. so Join https://t.me/IntellivoidDev and send #activateapi and follow instructions.			This Module also Needs MongoDB For a Storage of Some Data So make Sure you have that too.

Usage: .cf <as a reply to user's message //Turns AI on For that user.

	   .delcf <as a reply to user's message //Turns AI off For that user.			

Credits: @Zero_cool7870 (For Writing This Module)

		 Zi Xing (For CoffeeHouse API)			

"""

import coffeehouse as cf

from coffeehouse.exception import CoffeeHouseError

from uniborg.util import admin_cmd

import asyncio

import logging

from time import time

from telethon import events

from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)

api_key = Config.LYDIA_API

# Initialise client

api_client = cf.API(api_key)

cl = MongoClient(Config.MONGO_URI)

db = cl['test']

lydia = db.lydia

@borg.on(admin_cmd(pattern="cf", allow_sudo=True))

async def lydia_search(event):

	if event.fwd_from:

		return

	if event.reply_to_msg_id == None:

		await event.edit("Reply To A User's Message to Add him/her in Lydia Auto-Chat.")

		return	 	

	reply_msg = await event.get_reply_message()	

	user_id = reply_msg.from_id

	chat_id = event.chat_id

	await event.edit("Processing...")

	cursors = lydia.find({})

	try:

		for c in cursors:

			if c['user_id'] == user_id and c['chat_id'] == chat_id:

				await event.edit("User is already in Lydia Auto-Chat.")

				return		

	except:

		pass						

	session = api_client.create_session()

	ses = {'id':session.id,'expires':session.expires}

	logging.info(ses)

	lydia.insert_one({'user_id':user_id,'chat_id':chat_id,'session':ses})

	await event.edit("Lydia AI Turned On for User: "+str(user_id))

@borg.on(admin_cmd(pattern="delcf", allow_sudo=True))

async def lydia_search(event):

	if event.fwd_from:

		return

	if event.reply_to_msg_id == None:

		await event.edit("Reply To A User's Message to Remove him/her from Lydia Auto-Chat.")

		return	 		 

	reply_msg = await event.get_reply_message()	

	user_id = reply_msg.from_id

	chat_id = event.chat_id

	await event.edit("Processing...")

	cursors = lydia.find({})

	for c in cursors:

		if c['user_id'] == user_id and c['chat_id'] == chat_id:

			lydia.delete_one(c)

	await event.edit("Lydia AI Turned OFF for User: "+str(user_id))			

	

@borg.on(events.NewMessage())  

async def Lydia_bot_update(event):

	if event.fwd_from:

		return

	if event.media == None:	

		cursor = lydia.find({})

		for c in cursor:

			if c['user_id'] == event.from_id and c['chat_id'] == event.chat_id:

				query = event.text

				ses = c['session']

	

                # Check if the session is expired

                # If this method throws an exception at this point, then there's an issue with the API, Auth or Server.

				if ses['expires'] < time():

					session = api_client.create_session()

					ses = {'id': session.id, 'expires': session.expires}

					logging.info(ses)

					lydia.update_one(c,{'$set':{'user_id':event.from_id,'chat_id':event.chat_id,'session':ses}})			

    

                # Try to think a thought.            

				try:

					async with borg.action(event.chat_id, "typing"):

						await asyncio.sleep(1)

						output = api_client.think_thought(ses['id'],query)

						await event.reply(output)

				except CoffeeHouseError as e:

                    # CoffeeHouse related issue, session issue most likely.

					logging.error(str(e))

                    # Create a new session

					session = api_client.create_session()

					ses = {'id': session.id, 'expires': session.expires}

					logging.info(ses)

					lydia.update_one(c,{'$set':{'user_id':event.from_id,'chat_id':event.chat_id,'session':ses}})			

	

                    # Reply again, if this method fails then there's a other issue.

					async with borg.action(event.chat_id, "typing"):

						await asyncio.sleep(1)

						output = api_client.think_thought(ses['id'],query)

						await event.reply(output)
