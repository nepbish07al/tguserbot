# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting information about the server. """

from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from platform import python_version, uname
from shutil import which
from os import remove, system
from telethon import version
from subprocess import check_output
from telethon.tl.types import User, Chat, Channel

from userbot import CMD_HELP, ALIVE_NAME
from userbot.events import register, errors_handler

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@register(outgoing=True, pattern="^.sysd$")
@errors_handler
async def sysdetails(sysd):
    """ For .sysd command, get system info using neofetch. """
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            neo = "neofetch --stdout"
            fetch = await asyncrunapp(
                neo,
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())

            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("`Install neofetch first !!`")


@register(outgoing=True, pattern="^.botver$")
@errors_handler
async def bot_ver(event):
    """ For .botver command, get the bot version. """
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        if which("git") is not None:
            invokever = "git describe --all --long"
            ver = await asyncrunapp(
                invokever,
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await ver.communicate()
            verout = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())

            invokerev = "git rev-list --all --count"
            rev = await asyncrunapp(
                invokerev,
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await rev.communicate()
            revout = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())

            await event.edit("`Userbot Version: "
                             f"{verout}"
                             "` \n"
                             "`Revision: "
                             f"{revout}"
                             "`")
        else:
            await event.edit(
                "Shame that you don't have git, You're running 4.0 - 'Essentials' anyway"
            )


@register(outgoing=True, pattern="^.status$")
@errors_handler
async def amireallyalive(alive):
    """ For .alive command, check if the bot is running.  """
    
    rtt = check_output("ping -c 1 1.1.1.1 | grep -oP '.*time=\K(\d*\.\d*).*'", shell=True).decode()
    
    if not alive.text[0].isalpha() and alive.text[0] not in ("/", "#", "@",
                                                             "!"):
        await alive.edit("`"
                         "System Status: "
                         f"Online \n \n"
                         f"Telethon version: {version.__version__} \n"
                         f"Python: {python_version()} \n"
                         f"User: {DEFAULTUSER}\n"
                         f"RTT: {rtt}"
                         "`")


CMD_HELP.update(
    {"sysd": ".sysd\
    \nUsage: Shows system information using neofetch."})
CMD_HELP.update({"botver": ".botver\
    \nUsage: Shows the userbot version."})
CMD_HELP.update({
    "status":
    ".status\
    \nUsage: Type .status to see wether your bot is working or not."
})
