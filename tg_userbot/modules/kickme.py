from tg_userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID, bot
from tg_userbot.events import register
from asyncio import sleep
from tg_userbot.modules.admin import get_user_from_event

@register(outgoing=True, pattern="^\.kickme$")
async def kickme(leave):
    """ Basically it's .kickme command """
    await leave.edit("`Nope, no, no, I go away`")
    await sleep(0.1)
    await leave.client.kick_participant(leave.chat_id, 'me')

CMD_HELP.update({
    'kickme':
        '`.kickme\nUsage:- kicks you out of the group.`'
})
