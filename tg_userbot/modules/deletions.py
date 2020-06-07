from asyncio import sleep

from telethon.errors import rpcbaseerrors

from tg_userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from tg_userbot.events import register


@register(outgoing=True, pattern="^\.purge$")
async def fastpurger(purg):  # fast purge all messages up to tagged one
    if not purg.text[0].isalpha() and purg.text[0] in ("."):
        chat = await purg.get_input_chat()
        msgs = []
        count = 0
        async for msg in purg.client.iter_messages(
                chat, min_id=purg.reply_to_msg_id):
            msgs.append(msg)
            count = count + 1
            msgs.append(purg.reply_to_msg_id)
            if len(msgs) == 100:
                await purg.client.delete_messages(chat, msgs)
                msgs = []
        if msgs:
            await purg.client.delete_messages(chat, msgs)
        done = await purg.client.send_message(purg.chat_id,
                                              "`Fast purge complete!\n`Purged " + str(count) + " messages.")
        if BOTLOG:
            await purg.client.send_message(BOTLOG_CHATID, "Purge of " + str(count) + " messages done successfully.")
        await sleep(2)
        await done.delete()


@register(outgoing=True, pattern="^\.purgeme")
async def purgeme(delme):  # same as fast purge, but only your messages
    if not delme.text[0].isalpha() and delme.text[0] in ("."):
        message = delme.text
        count = int(message[9:])
        i = 1
        async for message in delme.client.iter_messages(delme.chat_id, from_user='me'):
            if i > count + 1:
                break
            i = i + 1
            await message.delete()
        smsg = await delme.client.send_message(delme.chat_id, "`Purge complete!` Purged " + str(count) + " messages.")
        if BOTLOG:
            await delme.client.send_message(BOTLOG_CHATID, "Purge of " + str(count) + " messages done successfully.")
        await sleep(2)
        i = 1
        await smsg.delete()


@register(outgoing=True, pattern="^\.del$")
async def delete_it(delme):
    if not delme.text[0].isalpha() and delme.text[0] in ("."):
        msg_src = await delme.get_reply_message()
        if delme.reply_to_msg_id:
            try:
                await msg_src.delete()
                await delme.delete()
                if BOTLOG:
                    await delme.client.send_message(BOTLOG_CHATID, "Deletion of message was successful")
            except rpcbaseerrors.BadRequestError:
                if BOTLOG:
                    await delme.client.send_message(BOTLOG_CHATID, "Well, I can't delete a message")


CMD_HELP.update({
    'deletions':
        '`.purge`\
         \nUsage: Purges all messages starting from the reply.\
         \n\n`.purgeme <x>`\
         \nUsage: Deletes x amount of your latest messages.\
         \n\n`.del`\
         \nUsage: Deletes the message replied to'
})
