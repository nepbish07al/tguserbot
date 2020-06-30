from tg_userbot import bot, CMD_HELP
from tg_userbot.events import register
from tg_userbot.modules.user_info import get_user

@register(outgoing=True, pattern="^\.mention(?: |$)(.*)")
async def permalink(mention):
    message = mention.pattern_match.group(1)
    args = message.split()
    user = await get_user(mention)
    fn = user.user.first_name
    if str(type(user)) != '<class \'telethon.tl.types.UserFull\'>':
        await mention.edit("`Can't mention someone who doesn't exist!`")
        return
    user = str(user.user.id)
    if len(args) >= 2:
        reason = str(message.split(' ', 1)[1])
    if len(args) == 1:
        reason = fn
    if len(args) == 0:
        await mention.edit("`Can't mention someone who doesn't exist!`")
    await mention.delete()
    await mention.respond(f'[{reason}](tg://user?id={user})')
