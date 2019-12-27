from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from platform import python_version, uname
from shutil import which
from os import remove, system
from telethon import version
from subprocess import check_output
from telethon.tl.types import User, Chat, Channel
from tg_userbot import CMD_HELP, ALIVE_NAME, BOTLOG, BOTLOG_CHATID, VERSION
from tg_userbot.events import register, errors_handler

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node

@register(outgoing=True, pattern="^.sysd$")
@errors_handler
async def sysdetails(sysd): #sysd command, requires neofetch
    if not sysd.text[0].isalpha() and sysd.text[0] in ("."):
        try:
            neo = "neofetch --stdout"
            fetch = await asyncrunapp(neo, stdout=asyncPIPE, stderr=asyncPIPE)
            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) + str(stderr.decode().strip())
            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("`Install neofetch first !!`")

@register(outgoing=True, pattern="^.status$")
@errors_handler
async def amireallyalive(alive): #.status, .alive, you name it
    if not alive.text[0].isalpha() and alive.text[0] in ("."):
        rtt = check_output("ping -c 1 1.1.1.1 | grep -oP '.*time=\K(\d*\.\d*).*'", shell=True).decode()
        await alive.edit("`"
                         "System Status: "
                         f"Online \n \n"
                         f"Telethon version: {version.__version__} \n"
                         f"Python: {python_version()} \n"
                         f"User: {DEFAULTUSER}\n"
                         f"RTT: {rtt}"
                         "`")

@register(outgoing=True, pattern="^.shutdown$")
@errors_handler
async def killdabot(event): #bot shutdown
    if not event.text[0].isalpha() and event.text[0] in ("."):
        await event.edit("`Powering off...`")
        if BOTLOG:
            await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n""Bot shut down")
        await event.client.disconnect()

CMD_HELP.update(
    {"systools": ".sysd\
    \nUsage: Shows system information using neofetch.\
    \n.status\
    \nUsage: Type .status to see wether your bot is working or not.\
    \n.shutdown\
    \nUsage: Type .shutdown to shutdown the bot."})
