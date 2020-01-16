import os
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from tg_userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, HOMIES, GIRLFRIEND, OWNER_ID
from tg_userbot.events import register, errors_handler

@register(pattern=".info(?: |$)(.*)", outgoing=True)
@errors_handler
async def who(event): #.info command
    if not event.text[0].isalpha() and event.text[0] in ("."):
        if event.fwd_from:
            return
        await event.edit("`Calling Mark Zuckerburg...`")
        if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
            os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
        replied_user = await get_user(event)
        caption = await fetch_info(replied_user, event)
        message_id_to_reply = event.message.reply_to_msg_id
        if not message_id_to_reply:
            message_id_to_reply = None
        try:
            await event.client.send_file(event.chat_id, caption=caption, link_preview=False, force_document=False, reply_to=message_id_to_reply, parse_mode="html")
            await event.delete()
        except TypeError:
            await event.edit(caption, parse_mode="html")

async def get_user(event): #fetch user, Zuckerburg's phone call
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

async def fetch_info(replied_user, event):
    replied_user_profile_photos = await event.client(GetUserPhotosRequest(user_id=replied_user.user.id, offset=42, max_id=0,limit=80))
    replied_user_profile_photos_count = "Person needs help with uploading profile picture."
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
    common_chat = str(replied_user.common_chats_count)
    if user_id == OWNER_ID:
        common_chat = "really, mate?"
    username = replied_user.user.username
    user_bio = replied_user.about
    is_bot = replied_user.user.bot
    restricted = replied_user.user.restricted
    verified = replied_user.user.verified
    first_name = first_name.replace("\u2060", "") if first_name else ("(N/A)")
    last_name = last_name.replace("\u2060", "") if last_name else ("(N/A)")
    join_date = member_obj.date if member_obj is not None and hasattr(member_obj, "date") else None
    username = "@{}".format(username) if username else ("(N/A)")
    user_bio = "This User has no About" if not user_bio else user_bio
    caption = "<b>USER INFO:</b>\n\n"
    caption += f"First Name: {first_name}\n"
    caption += f"Last Name: {last_name}\n"
    caption += f"Username: {username}\n"
    if user_id in HOMIES:
        caption +=f"\nThis is one of my homies, respect him!\n\n"
    elif user_id == GIRLFRIEND:
        caption +=f"\nThis is my girlfriend, leave her alone or you will get in trouble!\n\n"
    caption += f"Data Centre ID: {dc_id}\n"
    caption += f"Number of Profile Pics: {replied_user_profile_photos_count}\n"
    caption += f"Permanent Link To Profile: "
    caption += f"<a href=\"tg://user?id={user_id}\">{first_name}</a>\n"
    caption += f"Is Bot: {is_bot}\n"
    caption += f"Is Restricted: {restricted}\n"
    caption += f"Join date: {join_date}\n"
    caption += f"Is Verified by Telegram: {verified}\n"
    caption += f"ID: <code>{user_id}</code>\n\n"
    caption += f"Bio: \n<code>{user_bio}</code>\n\n"
    caption += f"Common Chats with this user: {common_chat}\n"
    return caption

CMD_HELP.update({
    "user_info":
    ".info <username> or as a reply to someones text\
    \nUsage: Gets info of an user."})
