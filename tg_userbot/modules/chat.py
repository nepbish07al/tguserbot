from time import sleep

from tg_userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID, bot
from tg_userbot.events import register, errors_handler


@register(outgoing=True, pattern="^\.userid$")
@errors_handler
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
@errors_handler
async def chatidgetter(chat):  # gets chat id
    if not chat.text[0].isalpha() and chat.text[0] in ("."):
        await chat.edit("Chat ID: `" + str(chat.chat_id) + "`")


@register(outgoing=True, pattern=r"^\.log(?: |$)([\s\S]*)")
@errors_handler
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


CMD_HELP.update({
    "chat":
        "`.chatid`\
    \nUsage: Fetches the current chat's ID\
    \n\n`.userid`\
    \nUsage: Fetches the ID of the user in reply, if its a forwarded message, finds the ID for the source.\
    \n\n`.log`\
    \nUsage: Forwards the message you've replied to in your bot logs group."})
