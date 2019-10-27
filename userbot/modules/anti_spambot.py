# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
''' A module for helping ban group join spammers. '''

from os import path
from asyncio import sleep
from requests import get
from pySmartDL import SmartDL
from telethon.errors import ChatAdminRequiredError
from telethon.events import ChatAction
from telethon.tl.types import ChannelParticipantsAdmins, Message, User

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, ANTI_SPAMBOT, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import errors_handler, register


@bot.on(ChatAction)
@errors_handler
async def ANTI_SPAMBOT_JOINED(welcm):
    try:
        ''' Ban a recently joined user if it
            matches the spammer checking algorithm. '''
        if not ANTI_SPAMBOT:
            return

        if welcm.user_joined or welcm.user_added:
            adder = None
            ignore = False
            users = None

            if welcm.user_added:
                ignore = False
                try:
                    adder = welcm.action_message.from_id
                except AttributeError:
                    return

            async for admin in bot.iter_participants(
                    welcm.chat_id, filter=ChannelParticipantsAdmins):
                if admin.id == adder:
                    ignore = True
                    break

            if ignore:
                return

            elif welcm.user_joined:
                users_list = hasattr(welcm.action_message.action, "users")
                if users_list:
                    users = welcm.action_message.action.users
                else:
                    users = [welcm.action_message.from_id]

            await sleep(5)
            spambot = False

            if not users:
                return

            for user_id in users:
                async for message in bot.iter_messages(welcm.chat_id,
                                                       from_user=user_id,
                                                       limit=1):

                    correct_type = isinstance(message, Message)
                    if not message:
                        break

                    join_time = welcm.action_message.date
                    message_date = message.date

                    if message_date < join_time:
                        continue  # The message was sent before the user joined, thus ignore it

                    check_user = await welcm.client.get_entity(user_id)

                    # DEBUGGING. LEAVING IT HERE FOR SOME TIME ###
                    print(
                        f"\nUser Joined: {check_user.first_name} [ID: {check_user.id}]"
                    )
                    print(f"Chat: {welcm.chat.title}")
                    print(f"Time: {join_time}")
                    print(
                        f"Message Sent: {message.text}\n[Time: {message_date}]\n"
                    )
                    ##############################################

                    try:
                        cas_url = f"https://combot.org/api/cas/check?user_id={check_user.id}"
                        r = get(cas_url, timeout=3)
                        data = r.json()
                    except BaseException:
                        print(
                            "CAS check failed, falling back to legacy anti_spambot behaviour."
                        )
                        data = None
                        pass

                    if data and data['ok']:
                        reason = f"[CAS Banned](https://combot.org/cas/query?u={check_user.id})"
                        spambot = True
                    elif correct_type and "t.cn/" in message.text:
                        reason = "Match on `t.cn` URLs"
                        spambot = True
                    elif correct_type and "t.me/joinchat" in message.text:
                        reason = "Potential Promotion Message"
                        spambot = True
                    elif correct_type and message.fwd_from:
                        reason = "Forwarded Message"
                        spambot = True
                    elif correct_type and "?start=" in message.text:
                        reason = "Telegram bot `start` link"
                        spambot = True
                    elif correct_type and "bit.ly/" in message.text:
                        reason = "Match on `bit.ly` URLs"
                        spambot = True
                    else:
                        if check_user.first_name in ("Bitmex", "Promotion",
                                                     "Information", "Dex",
                                                     "Announcements", "Info"):
                            if user.last_name == "Bot":
                                reason = "Known spambot"
                                spambot = True

                    if spambot:
                        print(f"Potential Spam Message: {message.text}")
                        if ANTI_SPAMBOT == 2:
                            await message.delete()
                        break

                    continue  # Check the next messsage

            if spambot:
                if ANTI_SPAMBOT == 2:
                    try:
                        await welcm.client.kick_participant(welcm.chat_id, check_user.id)
                        await sleep(.5)
                        await welcm.reply("Potential Spambot Detected !!\n"
                                          f"REASON: {reason}\n"
                                          f"[{check_user.first_name}](tg://user?id={check_user.id}) has been kicked!")
                    except Exception as e:
                        await welcm.reply("Potential Spambot Detected !!\n"
                                          f"REASON: {reason}\n"
                                          "It's highly recommended to ban/kick this spammer")
                        print(e)

                if ANTI_SPAMBOT in (1, 2):
                    print("\nPotential Spambot Detected !!\n"
                          f"USER: {check_user.first_name}\n"
                          f"USER ID: {check_user.id}\n"
                          f"CHAT: {welcm.chat.title}\n"
                          f"CHAT ID: {welcm.chat_id}\n"
                          f"REASON: {reason}\n"
                          f"MESSAGE:\n{message.text}\n")

    except ValueError:
        pass


@register(outgoing=True, pattern="^.cascheck ?(.*)")
@errors_handler
async def cascheck(cas):
    """For .cascheck command, check a specific or list all CAS Banned users in a chat."""
    if cas.reply_to_msg_id:
        replied_msg = await cas.get_reply_message()
        chat = replied_msg.from_id
    else:
        chat = cas.pattern_match.group(1)

        if chat:
            try:
                chat = int(chat)
            except ValueError:
                pass

    if not chat:
        chat = cas.chat_id

    try:
        info = await cas.client.get_entity(chat)
    except (TypeError, ValueError) as err:
        await cas.edit(str(err))
        return

    await cas.edit("`Processing...`")
    exportcsv = TEMP_DOWNLOAD_DIRECTORY + "/export.csv"
    user_ids = []
    if path.exists(exportcsv):
        with open(exportcsv) as data:
            for cas_id in data:
                user_ids.append(int(cas_id))
    else:
       await cas.edit("`CAS data not found. Please use .casupdate command to get the latest CAS data`")
       return

    try:
        if type(info) is User:  # check an user only
            if info.id in user_ids:
                if not info.deleted:
                    text = f"Warning! [{info.first_name}](tg://user?id={info.id}) [ID: `{info.id}`] is CAS Banned!"
                else:
                    text = f"Warning! Deleted Account [ID: `{info.id}`] is CAS Banned!"
            else:
                text = f"[{info.first_name}](tg://user?id={info.id}) is not CAS Banned"
        else:  # check for all members in a chat
            title = info.title if info.title else "this chat"
            cas_count, members_count = (0,)*2
            text_users = ""
            async for user in cas.client.iter_participants(info.id):
                if user.id in user_ids:
                    cas_count += 1
                    if not user.deleted:
                        text_users += f"\n{cas_count}. [{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    else:
                        text_users += f"\n{cas_count}. Deleted Account `{user.id}`"
                members_count += 1
            text = "Warning! `{}` of `{}` users are CAS Banned in **{}**:\n".format(cas_count, members_count, title)
            text += text_users
            if not cas_count:
                text = f"`No CAS Banned users found in {title}`"
    except ChatAdminRequiredError as carerr:
        await cas.edit("`CAS check failed: Admin privileges are required`")
        print("ChatAdminRequiredError:", carerr)
        return
    except BaseException as be:
        await cas.edit("`CAS check failed`")
        print("BaseException:", be)
        return
    finally:
        data.close()

    await cas.edit(text)


@register(outgoing=True, pattern="^.casupdate$")
@errors_handler
async def casupdate(down):
    """For casupdate command, download the latest export.csv from combot.org"""
    url = "https://combot.org/api/cas/export.csv"
    filename = TEMP_DOWNLOAD_DIRECTORY + "/export.csv"
    downloader = SmartDL(url, filename, progress_bar=False, connect_default_logger=True)
    await down.edit("`Connecting...`")
    downloader.start(blocking=False)
    await down.edit("`Downloading...`")
    if downloader.isSuccessful():
        await down.edit("`Successfully updated latest CAS CSV data`")
        print("CASUPATE status: %s" % downloader.get_status())
        print("CASUPATE download time: %s seconds" % round(downloader.get_dl_time(), 2))
    else:
        print("CASUPATE status: %s" % downloader.get_status())
        await down.edit("`Download failed: Incorrect URL or {} not reachable`".format(url))
        for error in downloader.get_errors():
            print(str(error))
    return


CMD_HELP.update({
    'anti_spambot':
    "If enabled in config.env or env var,\
        \nthis module will kick (or inform the admins of the group about) the\
        \nspammer(s) if they match the userbot's anti-spam algorithm.\
    \n\n.cascheck [optional <reply/user id/username/chat id/invite link>]\
    \nAllows you to check an user, channel (with admin flag) or a whole group for CAS Banned users.\
    \n\n.casupdate\
    \nGet the latest CAS CSV list from combot.org. Required for .cascheck."
})
