from os import path
from asyncio import sleep
from requests import get
from pySmartDL import SmartDL
from telethon.errors import ChatAdminRequiredError
from telethon.events import ChatAction
from telethon.tl.types import ChannelParticipantsAdmins, Message, User
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import errors_handler, register

@register(outgoing=True, pattern="^.cascheck ?(.*)")
@errors_handler
async def cascheck(cas): #checks with combot api for banned users
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
async def casupdate(down): #downloads csv from combot export
    if not down.text[0].isalpha() and down.text[0] in ("."):
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
    ".cascheck [optional <reply/user id/username/chat id/invite link>]\
    \nAllows you to check an user, channel (with admin flag) or a whole group for CAS Banned users.\
    \n\n.casupdate\
    \nGet the latest CAS CSV list from combot.org. Required for .cascheck."
})
