"""Lydia AI plugin for @UniBorg

.enacf <as a reply to user's message //Turns AI on For that user.
.delcf <as a reply to user's message //Turns AI off For that user.
.lstcf // Outputs List Of Currently added Users in AI Auto-Chat.

Description: A module that Act as a chatbot and chat with a User/other Bot.
This Module Needs CoffeeHouse API to work. so Join https://telegram.dog/IntellivoidDev and send #activateapi and follow instructions.
This Module also Needs DB_URI For Storage of Some Data So make sure you have that too.

Credits:
@Hackintosh5 (for inspiring me to write this module)
@Zero_cool7870 (For Writing The Original Module)
@loxxi for modifications
Zi Xing (For CoffeeHouse API)"""


import coffeehouse as cf

import asyncio
import io
from sql_helpers.lydia_ai_sql import get_s, get_all_s, add_s, remove_s
from time import time
from uniborg.util import admin_cmd

if Config.LYDIA_API is not None:
    api_key = Config.LYDIA_API
    # Initialise client
    api_client = cf.API(api_key)


@borg.on(admin_cmd(pattern="(ena|del|lst)cf", allow_sudo=True))
async def lydia_disable_enable(event):
    if event.fwd_from:
        return
    if Config.LYDIA_API is None:
        await event.edit("please add required `LYDIA_API` env var")
        return
    if event.reply_to_msg_id is not None:
        input_str = event.pattern_match.group(1)
        reply_msg = await event.get_reply_message()
        user_id = reply_msg.from_id
        chat_id = event.chat_id
        await event.edit("Processing...")
        if input_str == "ena":
            session = api_client.create_session()
            logger.info(session)
            logger.info(add_s(user_id, chat_id, session.id, session.expires))
            await event.edit(f"Lydia AI turned on for [user](tg://user?id={user_id}) in chat: `{chat_id}`")
        elif input
