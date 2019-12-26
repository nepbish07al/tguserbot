import asyncio
from asyncio import wait, sleep
from tg_userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from tg_userbot.events import register, errors_handler

@register(outgoing=True, pattern="^.tspam (.*)")
@errors_handler
async def tmeme(e):
    if not e.text[0].isalpha() and e.text[0] in ("."):
        tspam = str(e.pattern_match.group(1))
        message = tspam.replace(" ", "")
        for letter in message:
            await e.respond(letter)
        await e.delete()
        if BOTLOG:
            await e.client.send_message(BOTLOG_CHATID, "#TSPAM \n\nTSpam was executed successfully")

@register(outgoing=True, pattern="^.spam (.*)")
@errors_handler
async def spammer(e):
    if not e.text[0].isalpha() and e.text[0] in ("."):
        counter = int(e.pattern_match.group(1).split(' ', 1)[0])
        spam_message = str(e.pattern_match.group(1).split(' ', 1)[1])
        await asyncio.wait([e.respond(spam_message) for i in range(counter)])
        await e.delete()
        if BOTLOG:
            await e.client.send_message(BOTLOG_CHATID, "#SPAM \n\nSpam was executed successfully")

CMD_HELP.update({
    "spam":
    ".tspam <text>\
\nUsage: Spam the text letter by letter.\
\n\n.spam <count> <text>\
\nUsage: Floods text in the chat !!\
\n\n\nNOTE : Spam at your own risk !!"})
