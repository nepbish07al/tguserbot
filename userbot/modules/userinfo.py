# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# The entire source code is OSSRPL except 'whois' (userinfo) which is MPL
# License: MPL and OSSRPL
""" Userbot module for getting info about any user on Telegram(including you!). """

import os

from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from psycopg2 import connect
from os import system
from userbot import CMD_HELP, OWNER_ID, DB_URI, HOMIE_LIST
from userbot.events import register, errors_handler


@register(pattern=".info(?: |$)(.*)", outgoing=True)
@errors_handler
async def info(event):
    await event.edit(
        "`Sit tight while I steal some data from Mark Zuckerburg...`")

    replied_user = await get_user(event)

    caption = await fetch_info(replied_user, event)

    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        message_id_to_reply = None

    try:
        await event.client.send_file(event.chat_id,
                                     caption=caption,
                                     link_preview=False,
                                     force_document=False,
                                     reply_to=message_id_to_reply,
                                     parse_mode="html")

    except TypeError:
        await event.edit(caption, parse_mode="html")


async def get_user(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(
                GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return replied_user


async def fetch_info(replied_user, event):
    """ Get details from the User object. """
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(user_id=replied_user.user.id,
                             offset=42,
                             max_id=0,
                             limit=80))
    replied_user_profile_photos_count = None
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError as e:
        pass
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception as e:
        dc_id = "Unknown"
        location = str(e)
    common_chat = replied_user.common_chats_count
    username = replied_user.user.username
    user_bio = replied_user.about
    user_deleted = replied_user.user.deleted
    is_bot = "<b>Yes</b>" if replied_user.user.bot else "No"
    restricted = "<b>Yes</b>" if replied_user.user.restricted else "No"
    verified = "<b>Yes</b>" if replied_user.user.verified else "No"

    db_valid = None
    try:
    	db_valid = connect(DB_URI)
    except:
    	pass

    if db_valid:
        from userbot.modules.sql_helper.gmute_sql import is_gmuted
        gmuted = is_gmuted(user_id)
    else:
        gmuted = None

    first_name = first_name.replace(
        "\u2060", "") if first_name else None
    last_name = last_name.replace(
        "\u2060", "") if last_name else None
    username = "@{}".format(username) if username else None
    user_gmuted = "No" if gmuted is not None else "Unknown"
    user_blocked = "<b>Yes</b>" if replied_user.blocked else "No"

    if replied_user.user.bot:
        known_cmds_temp = []
        known_cmds = None
        if replied_user.bot_info.commands is not None:
            for cmd in replied_user.bot_info.commands:
                known_cmds_temp.append(cmd.command)
        if known_cmds_temp:
            known_cmds = str(known_cmds_temp).strip("[]")

    if gmuted is not None:
        for x in gmuted:
    	    if x.sender == str(user_id):
                user_gmuted = "<b>Yes</b>"
                break

    caption = "<b>USER INFO:</b>\n"
    caption += f"ID: <code>{user_id}</code>\n"
    if first_name is not None:
        caption += f"First Name: {first_name}\n"
    if last_name is not None:
        caption += f"Last Name: {last_name}\n"
    if username is not None:
        caption += f"Username: {username}\n"
    if not user_deleted:
        caption += f"Permanent user link to stalk: "
        caption += f"<a href=\"tg://user?id={user_id}\">link</a>\n"
    caption += f"Data Centre ID: {dc_id}\n"
    if replied_user_profile_photos_count is not None:
        caption += f"Number of Profile Pics: {replied_user_profile_photos_count}\n"
    if user_id in HOMIE_LIST:
        caption += f"This dude is one of my homies! Show him some respect.\n"
    elif user_deleted:
    	caption += f"This person decided to leave Telegram. Account has been deleted.\n"
    if not user_id == OWNER_ID:
    	caption += f"\nBlocked: {user_blocked}\n\n"
    else:
    	caption += "\n"
    caption += f"Bot: {is_bot}\n"
    if replied_user.user.bot and replied_user.user.bot_info_version is not None:
    	caption += f"> Info version: {replied_user.user.bot_info_version}\n"
    	caption += f"> Commands: <code>{known_cmds}</code>\n\n"
    else:
    	caption += "\n"
    if not user_id == OWNER_ID and not user_id in HOMIE_LIST:
        caption += f"Globally muted: {user_gmuted}\n\n"
    caption += f"Restricted: {restricted}\n"
    if replied_user.user.restricted:
        caption += f"> Platform: {replied_user.user.restriction_reason[0].platform}\n"
        caption += f"> Reason: {replied_user.user.restriction_reason[0].reason}\n"
        caption += f"> Text: {replied_user.user.restriction_reason[0].text}\n\n"
    else:
    	caption += "\n"
    if replied_user.user.scam:
    	caption += "Scammer: <b>Yes</b>\n\n"
    caption += f"Verified by Telegram: {verified}\n\n"
    if user_bio:
        caption += f"Bio: \n<code>{user_bio}</code>\n\n"
    caption += f"Common Chats with this user"
    if replied_user.user.id == OWNER_ID:
    	caption += "... oh wait it's me lmao"
    else:
        caption += f": <code>{common_chat}</code>"

    return caption


CMD_HELP.update({
    "info":
    ".info <username> or reply to someones text with .info\
    \nUsage: Gets info of an user."
})
