from telethon.errors import ChatAdminRequiredError
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

import tg_userbot.modules.libs.cas_api as cas_api
from tg_userbot import CMD_HELP
from tg_userbot.events import register


async def get_user(event):  # kanged get user
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            self_user = await event.client.get_me()
            user = self_user.id
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return replied_user


@register(pattern="^\.cascheck(?: |$)(.*)", outgoing=True)
async def caschecker(event):
    if not event.text[0].isalpha() and event.text[0] in ("."):
        if event.fwd_from:
            return
        replied_user = await get_user(event)
        if replied_user is None:
            text = "Failed to extract a user from given data"
            await event.edit(text, parse_mode="html")
            return
        user_analysis = replied_user.user
        text = "<b>USER DATA</b>\n\n"
        text += "ID: " + str(user_analysis.id) + "\n"
        if user_analysis.first_name:
            text += "First name: " + str(user_analysis.first_name) + "\n"
        if user_analysis.last_name:
            text += "Last name: " + str(user_analysis.last_name) + "\n"
        if user_analysis.username:
            text += "Username: @" + str(user_analysis.username) + "\n"
        text += "\n<b>CAS DATA</b>\n\n"
        result = cas_api.banchecker(user_analysis.id)
        text += "Result: " + str(result) + "\n"
        if result:
            parsing = cas_api.offenses(user_analysis.id)
            if parsing:
                text += "Total of Offenses: "
                text += str(parsing)
                text += "\n"
            parsing = cas_api.timeadded(user_analysis.id)
            if parsing:
                parseArray = str(parsing).split(", ")
                text += "Day added: "
                text += str(parseArray[1])
                text += "\nTime added: "
                text += str(parseArray[0])
                text += "\n\nAll times are in UTC"
        await event.edit(text, parse_mode="html")
        return


@register(pattern="^\.groupcheck$", outgoing=True)
async def groupchecker(cas):
    if not cas.text[0].isalpha() and cas.text[0] in ("."):
        text = ""
        chat = cas.chat_id
        try:
            info = await cas.client.get_entity(chat)
        except (TypeError, ValueError) as err:
            await cas.edit(str(err))
            return
        try:
            cas_count, members_count = (0,) * 2
            banned_users = ""
            async for user in cas.client.iter_participants(info.id):
                if cas_api.banchecker(user.id):
                    cas_count += 1
                    if not user.deleted:
                        banned_users += f"{user.first_name} {user.id}\n"
                    else:
                        banned_users += f"Deleted Account {user.id}\n"
                members_count += 1
            text = "Warning! `{}` of `{}` users are CAS Banned:\n".format(cas_count, members_count)
            text += banned_users
            if not cas_count:
                text = "No CAS Banned users found!"
        except ChatAdminRequiredError as carerr:
            await cas.edit("`CAS check failed: Admin privileges are required`")
            print("ChatAdminRequiredError:", carerr)
            return
        except BaseException as be:
            await cas.edit("`CAS check failed`")
            print("BaseException:", be)
            return
        await cas.edit(text)


CMD_HELP.update({
    "cas_interface":
        "`.cascheck` <reply/username/user id>\
        \nChecks the CAS Status of a specified user"})
