from tg_userbot import BOTLOG, BOTLOG_CHATID, AUTOMATION_ENABLED, AUTOMATION_SENDERS, AUTOMATION_COMMANDS, \
    AUTOMATION_TRIGGERS, CMD_HELP
from tg_userbot.events import register

AUTOMATOR_REPLIES = "Testing Automation again"


@register(incoming=True)
async def automator(sender):
    if AUTOMATION_ENABLED and sender.is_private and (sender.sender_id in AUTOMATION_SENDERS):
        value = 0
        for trigger in AUTOMATION_TRIGGERS:
            if trigger in sender.raw_text:
                commandId = AUTOMATION_TRIGGERS.index(trigger)
                command = AUTOMATION_COMMANDS[commandId]
                x = sender.raw_text.split(trigger)
                data = x[1]
                replyStr = command + " " + data + " " + AUTOMATOR_REPLIES
                await sender.reply(replyStr)
                if BOTLOG:
                    await sender.client.send_message(BOTLOG_CHATID,
                                                     "#AUTOMATION \n\n The command '" + replyStr + "' has been executed in " + str(
                                                         sender.sender_id))


CMD_HELP.update({
    "automation":
        "Automation is based of config settings for now.\
         \nPlease refer to your configuration settings or to tguserbot's owner manual."})
