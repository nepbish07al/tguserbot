from userbot import CMD_HELP
from userbot.events import register, errors_handler

@register(outgoing=True, pattern="^.help(?: |$)(.*)")
@errors_handler
async def help(event): #generates help message
    if not event.text[0].isalpha() and event.text[0] in ("."):
        args = event.pattern_match.group(1)
        if args:
            if args in CMD_HELP:
                await event.edit(str(CMD_HELP[args]))
            else:
                await event.edit("Please specify a valid module name.")
        else:
            await event.edit("Please specify which module do you want help for !!\nSyntax: .help <module name>")
            string = ""
            for i in CMD_HELP:
                string += "ℹ️ `" + str(i)
                string += "`\n"
            await event.reply(string)
