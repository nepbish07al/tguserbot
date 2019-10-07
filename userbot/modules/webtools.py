# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to the \
    Information Superhighway(yes, Internet). """

from datetime import datetime

import speedtest
from telethon import functions
from subprocess import check_output
from userbot import CMD_HELP
from userbot.events import register, errors_handler


@register(outgoing=True, pattern="^.speed$")
@errors_handler
async def speedtst(spd):
    if not spd.text[0].isalpha() and spd.text[0] in ("."):
        await spd.edit("`Running speed test . . .`")
        test = speedtest.Speedtest()

        test.get_best_server()
        test.download()
        test.upload()
        test.results.share()
        result = test.results.dict()

        await spd.edit("`"
                       "Started at "
                       f"{result['timestamp']} \n\n"
                       "Download "
                       f"{speed_convert(result['download'])} \n"
                       "Upload "
                       f"{speed_convert(result['upload'])} \n"
                       "Ping "
                       f"{result['ping']} \n"
                       "ISP "
                       f"{result['client']['isp']}"
                       "`")


def speed_convert(size):
    """
    Hi human, you can't read bytes?
    """
    power = 2**10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


@register(outgoing=True, pattern="^.dc$")
@errors_handler
async def neardc(event):
    if not event.text[0].isalpha() and event.text[0] in ("."):
        result = await event.client(functions.help.GetNearestDcRequest())
        await event.edit(f"Country : `{result.country}`\n"
                         f"Nearest Datacenter : `{result.nearest_dc}`\n"
                         f"This Datacenter : `{result.this_dc}`")

#Kanged .rtt from @prototype74, thanks homie
@register(outgoing=True, pattern="^.ping$")
@errors_handler
async def pingme(pong):
    if not pong.text[0].isalpha() and pong.text[0] in ("."):
        duration = check_output("ping -c 1 1.0.0.1 | grep -oP '.*time=\K(\d*\.\d*).*'", shell=True).decode()
        await pong.edit("`Ping speed is: %s`" % (duration))


@register(outgoing=True, pattern="^.cping(?: |$)?")
@errors_handler
async def cping(args):
    if not args.text[0].isalpha() and args.text[0] in ("."):
        commandParser = str(args.message.message).split(' ')
        if len(commandParser) != 2:
            await args.edit("`Bad arguments!`")
        else:
            dns = commandParser[1]
            #duration = check_output("ping -c 1 1.0.0.1 | grep -oP '.*time=\K(\d*\.\d*).*'", shell=True).decode()
            await args.edit("`DNS: " + dns +"`")

CMD_HELP.update(
    {"speed": ".speed\
    \nUsage: Does a speedtest and shows the results."})
CMD_HELP.update(
    {"dc": ".dc\
    \nUsage: Finds the nearest datacenter from your server."})
CMD_HELP.update(
    {"ping": ".ping\
    \nUsage: Shows your real time ping"})
