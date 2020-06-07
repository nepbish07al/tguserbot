import os
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from tg_userbot import CMD_HELP
from tg_userbot.events import register, errors_handler

async def get_id(event, userid):
    try:
        replied_user = await event.client(GetFullUserRequest(userid))
    except (TypeError, ValueError) as err:
        return str(err)
    return replied_user
