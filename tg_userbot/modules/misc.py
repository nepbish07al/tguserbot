from random import randint
from time import sleep
from os import execl
import sys
import os
import io
import sys
import json
from tg_userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from tg_userbot.events import register, errors_handler

@register(outgoing=True, pattern="^.shutdown$")
@errors_handler
async def killdabot(event): #bot shutdown
    if not event.text[0].isalpha() and event.text[0] in ("."):
        await event.edit("`Powering off...`")
        if BOTLOG:
            await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n""Bot shut down")
        await event.client.disconnect()

@register(outgoing=True, pattern="^.json$")
@errors_handler
async def json(event): #decodes message
    if not event.text[0].isalpha() and event.text[0] in ("."):
        the_real_message = None
        reply_to_id = None
        if event.reply_to_msg_id:
            previous_message = await event.get_reply_message()
            the_real_message = previous_message.stringify()
            reply_to_id = event.reply_to_msg_id
        else:
            the_real_message = event.stringify()
            reply_to_id = event.message.id
        with io.BytesIO(str.encode(the_real_message)) as out_file:
            out_file.name = "message.json"
            await event.client.send_file(event.chat_id, out_file, force_document=True, allow_cache=False, reply_to=reply_to_id, caption="`Here's the decoded message data !!`")
            await event.delete()

CMD_HELP.update({
    "shutdown":
    ".shutdown\
\nUsage: Simply .shutdown, equivalent to CTRL-C in terminal"})

CMD_HELP.update({
    "json":
    ".json\
\nUsage: Get detailed JSON formatted data about replied message"})
