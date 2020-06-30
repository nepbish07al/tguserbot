from telethon.tl.functions.users import GetFullUserRequest

from tg_userbot import bot, CMD_HELP, GBAN_BOTS, GBANS
from tg_userbot.events import register
from tg_userbot.modules.user_info import get_user


@register(outgoing=True, pattern=r"^.gban(?: |$)([\s\S]*)")
async def gban(request):
    if not request.text[0].isalpha() and request.text[0] in ("."):
        if GBANS:
            message = request.pattern_match.group(1)
            args = message.split()
            user = ''
            reason = ''
            response = ''
            user = await get_user(request)
            if str(type(user)) != '<class \'telethon.tl.types.UserFull\'>':
                await request.edit("`Lemme gban you for not giving a proper username!`")
                return
            user = str(user.user.id)
            if len(args) >= 2 and not request.reply_to_msg_id:
                reason = str(message.split(' ', 1)[1])
            elif len(args) == 1 and not request.reply_to_msg_id:
                reason = ""
            elif len(args) == 0 and not request.reply_to_msg_id:
                await request.edit("`Lemme gban you for not giving a proper username!`")
                return
            else:
                reason = message
            gbantext = '/gban ' + user + ' ' + reason
            for GBAN_BOT in GBAN_BOTS:
                async with bot.conversation(GBAN_BOT) as conv:
                    await conv.send_message(gbantext)
                    x = await conv.get_response()
                    if x:
                        pass
                    else:
                        x = GBAN_BOT + '  didn\'t respond'
                response += GBAN_BOT + ': ' + x.text.replace("**", "").replace("`", "").replace("tg://user?id=", "") + '\n\n'
            await request.edit("```" + response + "```")
        else:
            await request.edit("`You haven't enabled GBANS!`")


@register(outgoing=True, pattern=r"^.ungban(?: |$)([\s\S]*)")
async def ungban(request):
    if not request.text[0].isalpha() and request.text[0] in ("."):
        if GBANS:
            message = request.pattern_match.group(1)
            args = message.split()
            user = ''
            reason = message
            response = ''
            user = await get_user(request)
            if str(type(user)) != '<class \'telethon.tl.types.UserFull\'>':
                await request.edit("`Lemme gban you for not giving a proper username!`")
                return
            user = str(user.user.id)
            if len(args) >= 2 and not request.reply_to_msg_id:
                reason = str(message.split(' ', 1)[1])
            elif len(args) == 1 and not request.reply_to_msg_id:
                reason = ""
            elif len(args) == 0 and not request.reply_to_msg_id:
                await request.edit("`Lemme gban you for not giving a proper username!`")
                return
            else:
                reason = message 
            gbantext = '/ungban ' + user + ' ' + reason
            for GBAN_BOT in GBAN_BOTS:
                async with bot.conversation(GBAN_BOT) as conv:
                    await conv.send_message(gbantext)
                    x = await conv.get_response()
                    if x:
                        pass
                    else:
                        x = GBAN_BOT + '  didn\'t respond'
                response += GBAN_BOT + ': ' + x.text.replace("**", "").replace("`", "").replace("tg://user?id=", "") + '\n\n'
            await request.edit("```" + response + "```")
        else:
            await request.edit("`You haven't enabled GBANS!`")

@register(outgoing=True, pattern=r"^.gkick(?: |$)([\s\S]*)")
async def gkick(request):
    if not request.text[0].isalpha() and request.text[0] in ("."):
        if GBANS:
            message = request.pattern_match.group(1)
            args = message.split()
            user = ''
            reason = ''
            response = ''
            user = await get_user(request)
            if str(type(user)) != '<class \'telethon.tl.types.UserFull\'>':
                await request.edit("`Lemme gban you for not giving a proper username!`")
                return
            user = str(user.user.id)
            if len(args) >= 2 and not request.reply_to_msg_id:
                reason = str(message.split(' ', 1)[1])
            elif len(args) == 1 and not request.reply_to_msg_id:
                reason = ""
            elif len(args) == 0 and not request.reply_to_msg_id:
                await request.edit("`Lemme gban you for not giving a proper username!`")
                return
            else:
                reason = message
            gbantext = '/gkick ' + user + ' ' + reason
            for GBAN_BOT in GBAN_BOTS:
                async with bot.conversation(GBAN_BOT) as conv:
                    await conv.send_message(gbantext)
                    x = await conv.get_response()
                    if x:
                        pass
                    else:
                        x = GBAN_BOT + '  didn\'t respond'
                response += GBAN_BOT + ': ' + x.text.replace("**", "").replace("`", "").replace("tg://user?id=", "") + '\n\n'
            await request.edit("```" + response + "```")
        else:
            await request.edit("`You haven't enabled GBANS!`")

CMD_HELP.update({
    'gbans':
        '`.gban, .ungban, .gkick\nUsage: You\'ll know if you\'ve ever had a bot. Does exactly as it says.`'
})
