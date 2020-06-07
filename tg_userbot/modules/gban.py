import io
from tg_userbot import bot, CMD_HELP, GBAN_BOT, GBANS
from tg_userbot.events import register, errors_handler
from tg_userbot.modules.libs.get_id import get_id
from telethon.tl.functions.users import GetFullUserRequest

@register(outgoing=True, pattern=r"^.gban(?: |$)([\s\S]*)")
@errors_handler
async def gban(request):
    if not request.text[0].isalpha() and request.text[0] in ("."):
        if GBANS:
            message = request.pattern_match.group(1)
            args = message.split()
            user = ''
            reason = ''
            if request.reply_to_msg_id:
                previous_message = await request.get_reply_message()
                user = await request.client(GetFullUserRequest(previous_message.from_id))
                user = str(user.user.id)
                reason = message
                gbantext = '/gban '+user+' '+reason
            else:
                user = str(message.split(' ', 1)[0])
                user = await get_id(request, user)
                if str(type(user)) != '<class \'telethon.tl.types.UserFull\'>':
                    await request.edit("`Lemme gban you for not giving a proper username!`")
                    return
                user = str(user.user.id)
                if len(args) == 2:
                    reason = str(message.split(' ', 1)[1])
                if len(args) == 1:
                    reason = ""
                if len(args) == 0:
                    await request.edit("`Lemme gban you for not giving a proper username!`")
                gbantext = '/gban '+user+' '+reason
            async with bot.conversation(GBAN_BOT) as conv:
                await conv.send_message(gbantext)
                x = await conv.get_response()
                response = x.text.replace("**","").replace("`","").replace("tg://user?id=","")
                await request.edit("```"+response+"```")
        else:
            await request.edit("`You haven't enabled GBANS!`")


@register(outgoing=True, pattern=r"^.ungban(?: |$)([\s\S]*)")
@errors_handler
async def ungban(request):
    if not request.text[0].isalpha() and request.text[0] in ("."):
        if GBANS:
            message = request.pattern_match.group(1)
            args = message.split()
            user = ''
            if request.reply_to_msg_id:
                previous_message = await request.get_reply_message()
                user = await request.client(GetFullUserRequest(previous_message.from_id))
                user = str(user.user.id)
                gbantext = '/ungban '+user
            else:
                user = str(message.split(' ', 1)[0])
                user = await get_id(request, user)
                if str(type(user)) != '<class \'telethon.tl.types.UserFull\'>':
                    await request.edit("`Lemme gban you instead for not giving a proper username!`")
                    return
                user = str(user.user.id)
                if len(args) == 0:
                    await request.edit("`Lemme gban you instead for not giving a proper username!`")
                gbantext = '/ungban '+user
            async with bot.conversation(GBAN_BOT) as conv:
                await conv.send_message(gbantext)
                x = await conv.get_response()
                response = x.text.replace("**","").replace("`","").replace("tg://user?id=","")
                await request.edit("```"+response+"```")
        else:
            await request.edit("`You haven't enabled GBANS!`")


@register(outgoing=True, pattern=r"^.gkick(?: |$)([\s\S]*)")
@errors_handler
async def gkick(request):
    if not request.text[0].isalpha() and request.text[0] in ("."):
        if GBANS:
            message = request.pattern_match.group(1)
            args = message.split()
            user = ''
            reason = ''
            if request.reply_to_msg_id:
                previous_message = await request.get_reply_message()
                user = await request.client(GetFullUserRequest(previous_message.from_id))
                user = str(user.user.id)
                reason = message
                gbantext = '/gkick '+user+' '+reason
            else:
                user = str(message.split(' ', 1)[0])
                user = await get_id(request, user)
                if str(type(user)) != '<class \'telethon.tl.types.UserFull\'>':
                    await request.edit("`Dafaq am i gonna gkick you?!`")
                    return
                user = str(user.user.id)
                if len(args) == 2:
                    reason = str(message.split(' ', 1)[1])
                if len(args) == 1:
                    reason = ""
                if len(args) == 0:
                    await request.edit("`Dafaq am i gonna gkick you?!`")
                gbantext = '/gkick '+user+' '+reason
            async with bot.conversation(GBAN_BOT) as conv:
                await conv.send_message(gbantext)
                x = await conv.get_response()
                response = x.text.replace("**","").replace("`","").replace("tg://user?id=","")
                await request.edit("```"+response+"```")
        else:
            await request.edit("`You haven't enabled GBANS!`")

CMD_HELP.update({
    'gbans':
    '`.gban, .ungban, .gkick\nUsage: You\'ll know if you\'ve ever had a bot. Does exactly as it says.`'
})
