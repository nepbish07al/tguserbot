from asyncio import create_subprocess_shell as asyncrunapp
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from platform import python_version, uname
from subprocess import check_output
from shutil import which

from telethon import version

import tg_userbot.modules.libs.cas_api as cas
import tg_userbot.modules.libs.git_api as git
from tg_userbot import CMD_HELP, ALIVE_NAME, BOTLOG, BOTLOG_CHATID, VERSION, AUTOMATION_ENABLED
from tg_userbot.events import register

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node


@register(outgoing=True, pattern="^\.sysd$")
async def sysdetails(sysd):  # sysd command, requires neofetch
    if not sysd.text[0].isalpha() and sysd.text[0] in ("."):
        try:
            #neo = "neofetch --stdout"
            #fetch = await asyncrunapp(neo, stdout=asyncPIPE, stderr=asyncPIPE)
            #stdout, stderr = await fetch.communicate()
            #result = str(stdout.decode().strip()) + str(stderr.decode().strip())
            result = check_output("neofetch --stdout", shell=True).decode()
            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("`Install neofetch first !!`")

def pinger(address):
    if os.name == "nt":
        output = check_output("ping -n 1 " + address + " | findstr time*", shell=True).decode()
        outS = output.splitlines()
        out = outS[0]
    else:
        # out = check_output("ping -c 1 1.0.0.1 | grep -oP '.*time=\K(\d*\.\d*).*'", shell=True).decode()
        out = check_output("ping -c 1 " + address + " | grep time=", shell=True).decode()
    # duration = out
    splitOut = out.split(' ')
    under = False
    stringtocut = ""
    for line in splitOut:
        if (line.startswith('time=') or line.startswith('time<')):
            stringtocut = line
            break
    newstra = stringtocut.split('=')
    if len(newstra) == 1:
        under = True
        newstra = stringtocut.split('<')
    newstr = ""
    if os.name == 'nt':
        newstr = newstra[1].split('ms')
    else:
        newstr = newstra[1].split(' ')  # redundant split, but to try and not break windows ping
    ping_time = float(newstr[0])
    if os.name == 'nt' and under:
        return "<" + str(ping_time) + " ms"
    else:
        return str(ping_time) + " ms"

@register(outgoing=True, pattern="^\.botver$")
async def bot_ver(event):
    """ For .botver command, get the bot version. """
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        if which("git") is not None:
            ver = await asyncrunapp(
                "git",
                "describe",
                "--all",
                "--long",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await ver.communicate()
            verout = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())
 
            rev = await asyncrunapp(
                "git",
                "rev-list",
                "--all",
                "--count",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await rev.communicate()
            revout = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())
 
            await event.edit("`UserBot Version: "
                             f"{verout}"
                             "` \n"
                             "`Revision: "
                             f"{revout}"
                             f"\nTagged Version: {VERSION}"
                             "` \n")
        else:
            await event.edit(
                "Shame that you don't have git, you're running - " + VERSION + " anyway!"
            )


@register(outgoing=True, pattern="^\.status$")
async def statuschecker(msg):  # .status, .alive, you name it
    if not msg.text[0].isalpha() and msg.text[0] in ("."):
        gitver = git.vercheck()
        casver = cas.vercheck()
        rtt = pinger("1.0.0.1")
        automationData = "Disabled"
        commit = "N/A"
        if which("git") is not None:
            ver = await asyncrunapp(
                "git",
                "describe",
                "--all",
                "--long",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await ver.communicate()
            verout = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())
            verdiv = verout.split("-")
            commit = verdiv[2]
        if AUTOMATION_ENABLED:
            automationData = "Enabled"
        await msg.edit("`"
                       "System Status: "
                       f"Online \n \n"
                       f"Version: {VERSION}\n"
                       f"Commit: {commit}\n"
                       f"User: {DEFAULTUSER}\n"
                       f"RTT: {rtt}\n"
                       f"Automation: {automationData}\n"
                       f"\n"
                       f"Telethon: {version.__version__} \n"
                       f"Python: {python_version()} \n"
                       f"GitHub API: {gitver} \n"
                       f"CAS API: {casver}"
                       "`")


@register(outgoing=True, pattern="^\.shutdown$")
async def shutdown(event):  # bot shutdown
    if not event.text[0].isalpha() and event.text[0] in ("."):
        await event.edit("`Powering off...`")
        if BOTLOG:
            await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n""Bot shut down")
        await event.client.disconnect()


CMD_HELP.update(
    {"systools": "`.sysd`\
    \nUsage: Shows system information using neofetch.\
    \n\n`.status`\
    \nUsage: Type .status to see wether your bot is working or not.\
    \n\n`.botver`\
    \nUsage: Shows the userbot version.\
    \n\n`.shutdown`\
    \nUsage: Type .shutdown to shutdown the bot."})
