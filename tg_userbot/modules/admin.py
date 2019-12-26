from asyncio import sleep
from os import remove
from telethon.errors import BadRequestError, ChatAdminRequiredError, ImageProcessFailedError, PhotoCropSizeSmallError, UserAdminInvalidError, AdminsTooMuchError
from telethon.errors.rpcerrorlist import UserIdInvalidError, MessageTooLongError
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest, EditPhotoRequest
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import ChannelParticipantsAdmins, ChatAdminRights, ChatBannedRights, MessageEntityMentionName, MessageMediaPhoto, User
from tg_userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot, HOMIES
from tg_userbot.events import register, errors_handler

PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing the image`"
NO_ADMIN = "`I am not an admin!`"
NO_PERM = "`I don't have sufficient permissions!`"
CHAT_PP_CHANGED = "`Chat Picture Changed`"
INVALID_MEDIA = "`Invalid Extension`"

BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)
UNBAN_RIGHTS = ChatBannedRights(until_date=None, send_messages=None, send_media=None, send_stickers=None, send_gifs=None, send_games=None, send_inline=None, embed_links=None)
KICK_RIGHTS = ChatBannedRights(until_date=None, view_messages=True)

@register(outgoing=True, pattern="^.setgrouppic$")
@errors_handler
async def set_group_photo(gpic): #sets new group "profile" picture
    if not gpic.text[0].isalpha() and gpic.text[0] in ("."):
        replymsg = await gpic.get_reply_message()
        chat = await gpic.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        photo = None
        if not admin and not creator:
            await gpic.edit(NO_ADMIN)
            return
        if replymsg and replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await gpic.client.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split('/'):
                photo = await gpic.client.download_file(replymsg.media.document)
            else:
                await gpic.edit(INVALID_MEDIA)
        if photo:
            try:
                await gpic.client(EditPhotoRequest(gpic.chat_id, await gpic.client.upload_file(photo)))
                await gpic.edit(CHAT_PP_CHANGED)
            except PhotoCropSizeSmallError:
                await gpic.edit(PP_TOO_SMOL)
            except ImageProcessFailedError:
                await gpic.edit(PP_ERROR)

@register(outgoing=True, pattern="^.promote(?: |$)(.*)")
@errors_handler
async def promote(promt):
    if promt.text[0].isalpha() or promt.text[0] not in ("."):
        return
    chat = await promt.get_chat()
    if isinstance(chat, User):
        await promt.edit("`Yooo, this is not a channel or a group!`")
        return
    admin = chat.admin_rights  
    creator = chat.creator
    if not admin and not creator:
        await promt.edit(NO_ADMIN)
        return
    new_rights = ChatAdminRights(add_admins=False,
                                 invite_users=True,
                                 change_info=False,
                                 ban_users=True,
                                 delete_messages=True,
                                 pin_messages=True)
    get_user = await get_user_from_event(promt)
    if isinstance(get_user, tuple):
        user, rank = get_user
    else:
        user = get_user
        rank = ""
    if not rank:
        rank = ""
    if user:
        pass
    else:
        return
    if not isinstance(user, User):
        await promt.edit("`I can't promote a channel or a group!`")
        return
    try:
        async for member in promt.client.iter_participants(promt.chat_id, filter=ChannelParticipantsAdmins):
            if user.id == member.id:
                if user.is_self:
                    await promt.edit("`I am immortal already`")
                else:
                    await promt.edit("`This user is immortal already`")
                return
    except ChatAdminRequiredError as cadre:
        await promt.edit("`Admin privileges are required`")
        print("ChatAdminRequiredError:". cadre)
        return
    await promt.edit("`Promoting...`")
    try:
        if creator:
            await promt.client(
                EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        else:
            admin.add_admins = False
            if all(getattr(admin, right) is False for right in vars(admin)):
                return await promt.edit("`I don't have enough admin rights to promote this user`")
            await promt.client(
                EditAdminRequest(promt.chat_id, user.id, admin, rank))
        if user.id in HOMIES:
            await promt.edit("`Promoted my homie with immortal power!`")
        else:
            await promt.edit("`Promoted with immortal power!`")
    except AdminsTooMuchError as atme:
        await promt.edit("`There are too many admins in this chat already`")
        print("AdminsTooMuchError:", atme)
        return
    except BadRequestError as bre:
        await promt.edit(NO_PERM)
        print("BadRequestError:", bre)
        return
    except (TypeError, ValueError) as e:
        await promt.edit(str(e))
        return
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID, "#PROMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {promt.chat.title}(`{promt.chat_id}`)")

@register(outgoing=True, pattern="^.demote(?: |$)(.*)")
@errors_handler
async def demote(dmod):
    if dmod.text[0].isalpha() or dmod.text[0] not in ("."):
        return    
    chat = await dmod.get_chat()
    if isinstance(chat, User):
        await dmod.edit("`Yooo, this is not a channel or a group!`")
        return
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await dmod.edit(NO_ADMIN)
        return
    get_user = await get_user_from_event(dmod)
    if isinstance(get_user, tuple):
        user, rank = get_user
    else:
        user = get_user
        rank = ""
    if not rank:
        rank = ""
    if user:
        pass
    else:
        return
    if not isinstance(user, User):
        await dmod.edit("`I can't demote a channel or a group!`")
        return
    try:
        admins_list = []
        async for member in dmod.client.iter_participants(dmod.chat_id, filter=ChannelParticipantsAdmins):
            admins_list.append(member.id)
        if user.id not in admins_list:
            await dmod.edit("`This user is mortal already`")
            return
    except ChatAdminRequiredError as cadre:
        await dmod.edit("`Admin privileges are required`")
        print("ChatAdminRequiredError:". cadre)
        return
    if user.is_self:
        await dmod.edit("`I can't demote myself!`")
        return
    await dmod.edit("`Demoting...`")
    newrights = ChatAdminRights(add_admins=None,
                                invite_users=None,
                                change_info=None,
                                ban_users=None,
                                delete_messages=None,
                                pin_messages=None)
    try:
        await dmod.client(
            EditAdminRequest(dmod.chat_id, user.id, newrights, rank))
        await dmod.edit("`Demoted to a mortal user lmao`")
    except BadRequestError as bre:
        await dmod.edit(NO_PERM)
        print("BadRequestError:", bre)
        return
    except (TypeError, ValueError) as e:
        await dmod.edit(str(e))
        return
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID, "#DEMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {dmod.chat.title}(`{dmod.chat_id}`)")

@register(outgoing=True, pattern="^.ban(?: |$)(.*)")
@errors_handler
async def ban(bon): #bans tagged person
    if not bon.text[0].isalpha() and bon.text[0] in ("."):
        chat = await bon.get_chat() #sanity check, you know the drill already
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            await bon.edit(NO_ADMIN)
            return
        user = await get_user_from_event(bon)
        if user:
            pass
        else:
            return
        await bon.edit("`Banning user...`") #banning that cunt
        try:
            await bon.client(EditBannedRequest(bon.chat_id, user.id, BANNED_RIGHTS))
        except BadRequestError:
            await bon.edit(NO_PERM)
            return
        try:
            reply = await bon.get_reply_message()
            if reply:
                await reply.delete()
        except BadRequestError:
            await bon.edit("`I dont have message nuking rights! But still he was banned!`")
            return
        await bon.edit("`{}` was banned!".format(str(user.id)))
        if BOTLOG: #log shit
            await bon.client.send_message(
                BOTLOG_CHATID, "#BAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {bon.chat.title}(`{bon.chat_id}`)")

@register(outgoing=True, pattern="^.unban(?: |$)(.*)")
@errors_handler
async def nothanos(unbon): #unbans tagged person
    if not unbon.text[0].isalpha() and unbon.text[0] in ("."):
        chat = await unbon.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            await unbon.edit(NO_ADMIN)
            return
        await unbon.edit("`Unbanning...`")
        user = await get_user_from_event(unbon)
        if user:
            pass
        else:
            return
        try:
            await unbon.client(
                EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
            await unbon.edit("```Unbanned Successfully```")
            if BOTLOG:
                await unbon.client.send_message(
                    BOTLOG_CHATID, "#UNBAN\n"
                    f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                    f"CHAT: {unbon.chat.title}(`{unbon.chat_id}`)")
        except UserIdInvalidError:
            await unbon.edit("`Shit hit the fan! Ban failed!`")

@register(outgoing=True, pattern="^.delusers(?: |$)(.*)")
@errors_handler
async def rm_deletedacc(show): #lists/deletes deleted accounts
    if not show.text[0].isalpha() and show.text[0] in ("."):
        con = show.pattern_match.group(1)
        del_u = 0
        del_status = "`No deleted accounts found, Group is cleaned as Hell`" #Hell is full though, ain't it?
        if not show.is_group:
            await show.edit("`This command is only for groups!`")
            return
        if con != "clean":
            await show.edit("`Searching for zombie accounts...`")
            async for user in show.client.iter_participants(show.chat_id):
                if user.deleted:
                    del_u += 1
            if del_u > 0:
                del_status = f"found **{del_u}** deleted account(s) in this group.\nClean them by using .delusers clean"
            await show.edit(del_status)
            return
        chat = await show.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            await show.edit("`I am not an admin here!`")
            return
        await show.edit("`Deleting deleted accounts...\nOh I can do that?!?!`")
        del_u = 0
        del_a = 0
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                try:
                    await show.client(EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS))
                except ChatAdminRequiredError:
                    await show.edit("`I don't have ban rights in this group`")
                    return
                except UserAdminInvalidError:
                    del_u -= 1
                    del_a += 1
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
                del_u += 1
        if del_u > 0:
            del_status = f"cleaned **{del_u}** deleted account(s)"
        if del_a > 0:
            del_status = f"cleaned **{del_u}** deleted account(s) \
            \n**{del_a}** deleted admin accounts are not removed"
        await show.edit(del_status)
        if BOTLOG:
            await show.client.send_message(
                BOTLOG_CHATID, "#CLEANUP\n"
                f"Cleaned **{del_u}** deleted account(s) !!")

@register(outgoing=True, pattern="^.adminlist$")
@errors_handler
async def get_admin(show): #lists all chat admins
    if not show.text[0].isalpha() and show.text[0] in ("."):
        if not show.is_group:
            await show.edit("I don't think this is a group.")
            return
        info = await show.client.get_entity(show.chat_id)
        title = info.title if info.title else "this chat"
        mentions = f'<b>Admins in {title}:</b> \n'
        try:
            async for user in show.client.iter_participants(
                    show.chat_id, filter=ChannelParticipantsAdmins):
                if not user.deleted:
                    link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                    userid = f"<code>{user.id}</code>"
                    mentions += f"\n{link} {userid}"
                else:
                    mentions += f"\nDeleted Account <code>{user.id}</code>"
        except ChatAdminRequiredError as err:
            mentions += " " + str(err) + "\n"
        await show.edit(mentions, parse_mode="html")

@register(outgoing=True, pattern="^.pin(?: |$)(.*)")
@errors_handler
async def pin(msg): #pins message
    if not msg.text[0].isalpha() and msg.text[0] in ("."):
        chat = await msg.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            await msg.edit(NO_ADMIN)
            return
        to_pin = msg.reply_to_msg_id
        if not to_pin:
            await msg.edit("`Reply to a message to pin it.`")
            return
        options = msg.pattern_match.group(1)
        is_silent = True
        if options.lower() == "loud":
            is_silent = False
        try:
            await msg.client(UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
        except BadRequestError:
            await msg.edit(NO_PERM)
            return
        await msg.edit("`Pinned Successfully!`")
        user = await get_user_from_id(msg.from_id, msg)
        if BOTLOG:
            await msg.client.send_message(
                BOTLOG_CHATID, "#PIN\n"
                f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {msg.chat.title}(`{msg.chat_id}`)\n"
                f"LOUD: {not is_silent}")

@register(outgoing=True, pattern="^.kick(?: |$)(.*)")
@errors_handler
async def kick(usr): #kicks person
    if not usr.text[0].isalpha() and usr.text[0] in ("."):
        chat = await usr.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            await usr.edit(NO_ADMIN)
            return
        user = await get_user_from_event(usr)
        if not user:
            await usr.edit("`Couldn't fetch user.`")
            return
        await usr.edit("`Kicking...`")
        try:
            await usr.client(EditBannedRequest(usr.chat_id, user.id, KICK_RIGHTS))
            await sleep(.5)
        except BadRequestError:
            await usr.edit(NO_PERM)
            return
        await usr.client(EditBannedRequest(usr.chat_id, user.id, ChatBannedRights(until_date=None)))
        await usr.edit(f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`")
        if BOTLOG:
            await usr.client.send_message(
                BOTLOG_CHATID, "#KICK\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {usr.chat.title}(`{usr.chat_id}`)\n")

@register(outgoing=True, pattern="^.userslist ?(.*)")
@errors_handler
async def get_users(show): #lists all users (warning: spam)
    if not show.text[0].isalpha() and show.text[0] in ("."):
        if not show.is_group:
            await show.edit("Are you sure this is a group?")
            return
        info = await show.client.get_entity(show.chat_id)
        title = info.title if info.title else "this chat"
        mentions = 'Users in {}: \n'.format(title)
        try:
            if not show.pattern_match.group(1):
                async for user in show.client.iter_participants(show.chat_id):
                    if not user.deleted:
                        mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    else:
                        mentions += f"\nDeleted Account `{user.id}`"
            else:
                searchq = show.pattern_match.group(1)
                async for user in show.client.iter_participants(
                        show.chat_id, search=f'{searchq}'):
                    if not user.deleted:
                        mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    else:
                        mentions += f"\nDeleted Account `{user.id}`"
        except ChatAdminRequiredError as err:
            mentions += " " + str(err) + "\n"
        try:
            await show.edit(mentions)
        except MessageTooLongError:
            await show.edit("Damn, this is a huge group. Uploading users lists as file.")
            file = open("userslist.txt", "w+")
            file.write(mentions)
            file.close()
            await show.client.send_file(show.chat_id, "userslist.txt", caption='Users in {}'.format(title), reply_to=show.id)
            remove("userslist.txt")

async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`Pass the user's username, id or reply!`")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return user_obj

async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj

CMD_HELP.update({
    "admin":
    ".promote\
\nUsage: Reply to someone's message with .promote to promote them.\
\n\n.demote\
\nUsage: Reply to someone's message with .demote to revoke their admin permissions.\
\n\n.ban\
\nUsage: Reply to someone's message with .ban to ban them.\
\n\n.unban\
\nUsage: Reply to someone's message with .unban to unban them in this chat.\
\n\n.delusers\
\nUsage: Searches for deleted accounts in a group. Use .delusers clean to remove deleted accounts from the group.\
\n\n.adminlist\
\nUsage: Retrieves all admins in a chat.\
\n\n.userslist or .userslist <name>\
\nUsage: Retrieves all users in a chat.\
\n\n.kick\
\nUsage: Reply to someone's message with .kick to kick them."})
