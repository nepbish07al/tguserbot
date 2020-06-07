from tg_userbot import CMD_HELP
from tg_userbot.events import register


@register(outgoing=True, pattern="^.help(?: |$)(.*)")
async def help(event):  # generates help message
    if not event.text[0].isalpha() and event.text[0] in ("."):
        args = event.pattern_match.group(1)
        if args:
            if args in CMD_HELP:
                await event.edit(str(CMD_HELP[args]))
            else:
                await event.edit("Please specify a valid module name.")
        else:
            string = "Please specify which module do you want help for !!\nSyntax: .help <module name>\n\nModules available:\n\n"
            for i in CMD_HELP:
                string += "-> `" + str(i)
                string += "`\n"
            await event.edit(string)
