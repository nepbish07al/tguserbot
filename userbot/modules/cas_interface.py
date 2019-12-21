from asyncio import sleep
from datetime import datetime
from os import path, remove
from pySmartDL import SmartDL
from requests import get
from telethon.errors import ChatAdminRequiredError, ChatSendMediaForbiddenError
from telethon.errors.rpcerrorlist import MessageTooLongError
from telethon.events import ChatAction
from telethon.tl.types import ChannelParticipantsAdmins, Message, User
from urllib.error import HTTPError, URLError
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import errors_handler, register

import userbot.include.cas_api as cas_api

@register(outgoing=True, pattern="^.cascheck ?(.*)")
@errors_handler
async def cascheck(cas): #checks if a user, or all users in a group are cas banned
    if not cas.text[0].isalpha() and cas.text[0] in ("."):
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
        else:
            await cas.edit("`CAS data not found. Please use .casupdate command to get the latest CAS data`")
            return
        try:
            if type(info) is User:  # check an user only
                if cas_api.banchecker(info.id):
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
                    if cas_api.banchecker(user.id):
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
        try:
            await cas.edit(text)
        except MessageTooLongError as mtle:
            print("MessageTooLongError:", mtle)
            await cas.edit("`Jesus christ, there are too many CAS Banned users in this chat. Uploading list as a file...`")
            temp_file = open("caslist.txt", "w+")
            temp_file.write(text)
            temp_file.close()
            try:
                await cas.client.send_file(cas.chat_id, "caslist.txt")
            except ChatSendMediaForbiddenError as f:
                await cas.edit("`Failed to upload list: send media isn't allowed in this chat.`")
                print("ChatSendMediaForbiddenError:", f)
            except BaseException as be:
                await cas.edit("`Failed to upload list`")
                print("BaseException:", be)
            remove("caslist.txt")
            return

CMD_HELP.update({
    'anti_spambot':
    "If enabled in config.env or env var,\
        \nthis module will kick (or inform the admins of the group about) the\
        \nspammer(s) if they match the userbot's anti-spam algorithm.\
    \n\n.cascheck [optional <reply/user id/username/chat id/invite link>]\
    \nAllows you to check an user, channel (with admin flag) or a whole group for CAS Banned users."})
