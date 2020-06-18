from time import sleep
from telethon.errors import ChatAdminRequiredError, InputUserDeactivatedError, SearchQueryEmptyError
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputMessagesFilterEmpty

from tg_userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID, bot
from tg_userbot.events import register


@register(outgoing=True, pattern="^\.userid$")
async def useridgetter(target):  # gets user id
    if not target.text[0].isalpha() and target.text[0] in ("."):
        message = await target.get_reply_message()
        if message:
            if not message.forward:
                user_id = message.sender.id
                if message.sender.username:
                    name = "@" + message.sender.username
                else:
                    name = "**" + message.sender.first_name + "**"
            else:
                user_id = message.forward.sender.id
                if message.forward.sender.username:
                    name = "@" + message.forward.sender.username
                else:
                    name = "*" + message.forward.sender.first_name + "*"
            await target.edit("**Name:** {} \n**User ID:** `{}`".format(
                name, user_id))


@register(outgoing=True, pattern="^\.chatid$")
async def chatidgetter(chat):  # gets chat id
    if not chat.text[0].isalpha() and chat.text[0] in ("."):
        await chat.edit("Chat ID: `" + str(chat.chat_id) + "`")


@register(outgoing=True, pattern=r"^\.log(?: |$)([\s\S]*)")
async def log(log_text):  # forwards stuff to log channel/group
    if not log_text.text[0].isalpha() and log_text.text[0] in ("."):
        if BOTLOG:
            if log_text.reply_to_msg_id:
                reply_msg = await log_text.get_reply_message()
                await reply_msg.forward_to(BOTLOG_CHATID)
            elif log_text.pattern_match.group(1):
                user = f"#LOG / Chat ID: {log_text.chat_id}\n\n"
                textx = user + log_text.pattern_match.group(1)
                await bot.send_message(BOTLOG_CHATID, textx)
            else:
                await log_text.edit("`What am I supposed to log?`")
                return
            await log_text.edit("`Logged Successfully`")
        else:
            await log_text.edit(
                "`This feature requires Logging to be enabled!`")
        sleep(2)
        await log_text.delete()


@register(outgoing=True, pattern="^\.count(?: |$)(.*)")
async def countmessages(event):
    """ For .count, counts the total amount of messages from a certain user has sent in a chat. """
    if not event.text[0].isalpha() and event.text[0] in ("."):
        if not hasattr(event.message.to_id, "channel_id"):
            await event.edit("`Nope, it works in a channel or group only.`")
            return

        if event.reply_to_msg_id:
            message = await event.get_reply_message()
            user_id = message.sender.id if message.sender else None
            username = message.sender.username if message.sender and message.sender.username is not None else None
            first_name = message.sender.first_name if message.sender and  message.sender.first_name is not None else None
        else:
            arg = event.pattern_match.group(1)
            user = None

            if arg.isnumeric():
                arg = int(arg)

            if not arg:
                user = await event.client.get_me()
            else:
                try:
                    user = await event.client.get_entity(arg)
                except Exception as e:
                    print("Exception:", e)
                    await event.edit("`Failed to get user`")
                    return
            user_id = user.id
            username = user.username if user.username is not None else None
            first_name = user.first_name if user.first_name is not None else None

        try:
            msg_info = await event.client(SearchRequest(peer=event.chat_id,
                                                        q="",  # search for any message
                                                        filter=InputMessagesFilterEmpty(),
                                                        min_date=None,
                                                        max_date=None,
                                                        add_offset=0,
                                                        offset_id=0,
                                                        limit=0,
                                                        max_id=0,
                                                        min_id=0,
                                                        hash=0,
                                                        from_id=user_id))
        except ChatAdminRequiredError as care:
            print("ChatAdminRequiredError:", care)
            await event.edit("`Admin privileges are required!`")
            return
        except InputUserDeactivatedError as iude:
            print("InputUserDeactivatedError:", iude)
            await event.edit("`Can't count messages from a deleted user.`")
            return
        except SearchQueryEmptyError as sqee:
            print("SearchQueryEmptyError:", sqee)
            await event.edit("`Can't query forwarded messages from a channel.`")
            return
        except Exception as e:  # for all other cases
            print("Exception:", e)
            await event.edit("`Failed to count messages`")
            return

        name  = "@" + username if username else f"[{first_name}](tg://user?id={user_id})"

        if hasattr(msg_info, "count"):
            await event.edit(f"{name} has sent `{msg_info.count}` messages in this chat")
        else:
            await event.edit("`Can't count messages in this chat!`")

    return


@register(outgoing=True, pattern="^\.topusers(?: |$)(.*)")
async def topusers(event):
    """ For .topusers, lists the top active members in a chat. """
    if not event.text[0].isalpha() and event.text[0] in ("."):
        arg = event.pattern_match.group(1)
        chat = None

        try:
            arg = int(arg)
        except:
            pass

        if not arg and not hasattr(event.message.to_id, "channel_id"):
            await event.edit("`Nope, it works with channels and groups only.`")
            return

        if not arg:
            arg = event.chat_id

        try:
            chat = await event.client.get_entity(arg)
        except Exception as e:
            print("Exception:", e)
            await event.edit("`Failed to get chat`")
            return

        chat_id = chat.id
        chat_name = chat.title
        users = {}
        count = 0

        await event.edit("`Picking the most active members. This might take up some time...`")

        try:
            async for user in event.client.iter_participants(chat_id):
                # counting messages from deleted users would trigger InputUserDeactivatedError exception,
                # so skip them.
                if not user.deleted:
                    name  = "@" + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})"
                    if not name in users.keys():
                        msg_info = await event.client(SearchRequest(peer=chat_id,
                                                                    q="",  # search for any message
                                                                    filter=InputMessagesFilterEmpty(),
                                                                    min_date=None,
                                                                    max_date=None,
                                                                    add_offset=0,
                                                                    offset_id=0,
                                                                    limit=0,
                                                                    max_id=0,
                                                                    min_id=0,
                                                                    hash=0,
                                                                    from_id=user.id))
                        users[name] = msg_info.count  # add new key
            count = len(users.keys()) if len(users.keys()) < 10 else 10
            # sort the dictionary by highest value and limit it to 10 keys or lower
            users = {key: value for key, value in sorted(users.items(), key=lambda item: item[1], reverse=True)[:count]}
        except ChatAdminRequiredError as care:
            print("ChatAdminRequiredError:", care)
            await event.edit("`Admin privileges are required!`")
            return
        except Exception as e:  # for all other cases
            print("Exception:", e)
            await event.edit("`Failed to pick the most active members`")
            return

        text = "Top **{}** active members in **{}**:\n\n".format(count, chat_name)
        count = 1
        for key, value in users.items():
            text += "{}. {}: `{}` Messages\n".format(count, key, value)
            count += 1
        await event.edit(text)

    return


CMD_HELP.update({
    "chat":
        "`.chatid`\
    \nUsage: Fetches the current chat's ID\
    \n\n`.userid`\
    \nUsage: Fetches the ID of the user in reply, if its a forwarded message, finds the ID for the source.\
    \n\n`.log`\
    \nUsage: Forwards the message you've replied to in your bot logs group.\
    \n\n.count [optional: <reply/tag>]\
    \nUsage: Counts the messages from an user in a chat.\
    \n\n.topusers [optional: <tag/id>]\
    \nUsage: Lists the top members in a chat.\
    \nNote: The more members a chat have the longer the process takes."})
