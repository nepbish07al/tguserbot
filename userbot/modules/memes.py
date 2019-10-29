import asyncio
import random
import re
import time
from collections import deque
import requests
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from cowpy import cow
from userbot import CMD_HELP
from userbot.events import register, errors_handler

ZALG_LIST = [[
    "̖",
    " ̗",
    " ̘",
    " ̙",
    " ̜",
    " ̝",
    " ̞",
    " ̟",
    " ̠",
    " ̤",
    " ̥",
    " ̦",
    " ̩",
    " ̪",
    " ̫",
    " ̬",
    " ̭",
    " ̮",
    " ̯",
    " ̰",
    " ̱",
    " ̲",
    " ̳",
    " ̹",
    " ̺",
    " ̻",
    " ̼",
    " ͅ",
    " ͇",
    " ͈",
    " ͉",
    " ͍",
    " ͎",
    " ͓",
    " ͔",
    " ͕",
    " ͖",
    " ͙",
    " ͚",
    " ",
],
             [
                 " ̍",
                 " ̎",
                 " ̄",
                 " ̅",
                 " ̿",
                 " ̑",
                 " ̆",
                 " ̐",
                 " ͒",
                 " ͗",
                 " ͑",
                 " ̇",
                 " ̈",
                 " ̊",
                 " ͂",
                 " ̓",
                 " ̈́",
                 " ͊",
                 " ͋",
                 " ͌",
                 " ̃",
                 " ̂",
                 " ̌",
                 " ͐",
                 " ́",
                 " ̋",
                 " ̏",
                 " ̽",
                 " ̉",
                 " ͣ",
                 " ͤ",
                 " ͥ",
                 " ͦ",
                 " ͧ",
                 " ͨ",
                 " ͩ",
                 " ͪ",
                 " ͫ",
                 " ͬ",
                 " ͭ",
                 " ͮ",
                 " ͯ",
                 " ̾",
                 " ͛",
                 " ͆",
                 " ̚",
             ],
             [
                 " ̕",
                 " ̛",
                 " ̀",
                 " ́",
                 " ͘",
                 " ̡",
                 " ̢",
                 " ̧",
                 " ̨",
                 " ̴",
                 " ̵",
                 " ̶",
                 " ͜",
                 " ͝",
                 " ͞",
                 " ͟",
                 " ͠",
                 " ͢",
                 " ̸",
                 " ̷",
                 " ͡",
             ]]

EMOJIS = [
    "😂",
    "😂",
    "👌",
    "✌",
    "💞",
    "👍",
    "👌",
    "💯",
    "🎶",
    "👀",
    "😂",
    "👓",
    "👏",
    "👐",
    "🍕",
    "💥",
    "🍴",
    "💦",
    "💦",
    "🍑",
    "🍆",
    "😩",
    "😏",
    "👉👌",
    "👀",
    "👅",
    "😩",
    "🚰",
]

INSULT_STRINGS = [
    "When you were born, your mom thought she just had shit herself.",
    "Even a trained chimp does everything better than you.",
    "You know what is the difference between you and cancer? Cancer evolves.",
    "If you were in a room with Hitler and Stalin and I had a gun, I would shoot you twice.",
    "Your girlfriend could have picked a better man, like Saddam Hussein or an indonesian pimp with lice and bad breath.",
    "If stupidity was taxed, you would be all stamped.",
    "Light travels faster than sound, which explains why you seemed bright until you speak.",
    "Your teeth are like stars, light years away and yellow.",
    "Your face is like a treasure, it needs to be burried very deep.",
    "Why don't you slip into something more comfortable, like a coma?",
    "I will never forget the first time we met, although I am trying.",
    "If you were a bit more intelligent, you would still be stupid.",
    "Not even your IQ test is positive.",
    "I heard you are very kind to animals, so please return that face to the gorilla.",
    "You got your head so far up your ass, you can chew food twice.",
]

HELLOSTR = [
    "Hi !",
    "‘Ello, gov'nor!",
    "What’s crackin’?",
    "‘Sup, homeslice?",
    "Howdy, howdy ,howdy!",
    "Hello, who's there, I'm talking.",
    "You know who this is.",
    "Yo!",
    "Whaddup.",
    "Greetings and salutations!",
    "Hello, sunshine!",
    "Hey, howdy, hi!",
    "What’s kickin’, little chicken?",
    "Peek-a-boo!",
    "Howdy-doody!",
    "Hey there, freshman!",
    "I come in peace!",
    "Ahoy, matey!",
    "Hiya!",
]

SLAP_TEMPLATES = [
    "{hits} {victim} with **{item}**. {emoji}",
    "{hits} {victim} in the face with **{item}**. {emoji}",
    "{hits} {victim} around a bit with **{item}**. {emoji}",
    "{throws} **{item}** at {victim}. {emoji}",
    "grabs **{item}** and {throws} it at {victim}'s face. {emoji}",
    "launches **{item}** in {victim}'s general direction. {emoji}",
    "starts slapping {victim} silly with **{item}**. {emoji}",
    "pins {victim} down and repeatedly {hits} them with **{item}**. {emoji}",
    "grabs up **{item}** and {hits} {victim} with it. {emoji}",
    "ties {victim} to a chair and {throws} **{item}** at them. {emoji}",
]

ITEMS = (
    "a Samsung J5 2017",
    "a Samsung S10+",
    "an iPhone XS MAX",
    "a Note 9",
    "a Note 10+",
    "knox 0x0",
    "OneUI 2.0",
    "OneUI 69.0",
    "TwoUI 1.0",
    "Secure Folder",
    "Samsung Pay",
    "prenormal RMM state",
    "prenormal KG state",
    "a locked bootloader",
    "payment lock",
    "stock rom",
    "good rom",
    "Good Lock apps",
    "Q port",
    "Pie port",
    "8.1 port",
    "Pie port",
    "Pie OTA",
    "Q OTA",
    "LineageOS 16",
    "LineageOS 17",
    "a bugless rom",
    "a kernel",
    "a kernal",
    "a karnal",
    "a karnel",
    "official TWRP",
    "VOLTE",
    "kanged rom",
    "an antikang",
    "audio fix",
    "hwcomposer fix",
    "mic fix",
    "random reboots",
    "bootloops",
    "unfiltered logs",
    "a keylogger",
    "120FPS",
    "a download link",
    "168h uptime",
    "a paypal link",
    "treble support",
    "EVO-X gsi",
    "Q gsi",
    "Q beta",
    "a Rom Control",
    "a hamburger",
    "a cheeseburger",
    "a Big-Mac",
)

THROW = [
    "throws",
    "flings",
    "chucks",
    "hurls",
]

HIT = [
    "hits",
    "whacks",
    "slaps",
    "smacks",
    "spanks",
    "bashes",
]

EMOJI = (
    "\U0001F923",
    "\U0001F602",
    "\U0001F922",
    "\U0001F605",
    "\U0001F606",
    "\U0001F609",
    "\U0001F60E",
    "\U0001F929",
    "\U0001F623",
    "\U0001F973",
    "\U0001F9D0",
    "\U0001F632",
)

@register(outgoing=True, pattern=r"^.coinflip (.*)")
@errors_handler
async def coin(event):
    if not event.text[0].isalpha() and event.text[0] in ("."):
        if event.fwd_from:
            return
        r = random.randint(1, 100)
        input_str = event.pattern_match.group(1)
        if input_str:
            input_str = input_str.lower()
        if r % 2 == 1:
            if input_str == "heads":
                await event.edit(
                    "The coin landed on: **Heads**.\nYou were correct.")
            elif input_str == "tails":
                await event.edit(
                    "The coin landed on: **Heads**.\nYou weren't correct, try again ..."
                )
            else:
                await event.edit("The coin landed on: **Heads**.")
        elif r % 2 == 0:
            if input_str == "tails":
                await event.edit(
                    "The coin landed on: **Tails**.\nYou were correct.")
            elif input_str == "heads":
                await event.edit(
                    "The coin landed on: **Tails**.\nYou weren't correct, try again ..."
                )
            else:
                await event.edit("The coin landed on: **Tails**.")
        else:
            await event.edit("Gimme another coin, this one fake AF !!")

@register(pattern="^.slap(?: |$)(.*)", outgoing=True)
@errors_handler
async def who(event):
    if not event.text[0].isalpha() and event.text[0] in ("."):
        """ slaps a user, or get slapped if not a reply. """
        if event.fwd_from:
            return

        replied_user = await get_user(event)
        caption = await slap(replied_user, event)
        message_id_to_reply = event.message.reply_to_msg_id

        if not message_id_to_reply:
            message_id_to_reply = None

        try:
            await event.edit(caption)

        except BaseException:
            await event.edit(
                "`Can't slap this person, need to fetch some sticks and stones !!`"
            )

async def get_user(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(
                GetFullUserRequest(user_object.id))

        except (TypeError, ValueError):
            await event.edit("`I don't slap aliens, they ugly AF !!`")
            return None

    return replied_user

async def slap(replied_user, event):
    """ Construct a funny slap sentence !! """
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    username = replied_user.user.username

    if username:
        slapped = "@{}".format(username)
    else:
        slapped = f"[{first_name}](tg://user?id={user_id})"

    temp = random.choice(SLAP_TEMPLATES)
    item = random.choice(ITEMS)
    hit = random.choice(HIT)
    throw = random.choice(THROW)
    emoji = random.choice(EMOJI)

    caption = "..." + temp.format(
        victim=slapped, item=item, hits=hit, throws=throw, emoji=emoji)

    return caption

@register(outgoing=True, pattern="^.decide(?: |$)(.*)")
@errors_handler
async def decide(event):
    if not event.text[0].isalpha() and event.text[0] in ("."):
        if event.fwd_from:
            return
        message = event.pattern_match.group(1)
        message_id = None
        if event.reply_to_msg_id:
            message_id = event.reply_to_msg_id
        if not message:
            r = requests.get("https://yesno.wtf/api").json()
        else:
            try:
                r = requests.get(
                    f"https://yesno.wtf/api?force={message.lower()}").json()
            except BaseException:
                await event.edit("`Available decisions:` *yes*, *no*, *maybe*")
                return
        await event.client.send_message(event.chat_id,
                                        str(r["answer"]).upper(),
                                        reply_to=message_id,
                                        file=r["image"])
        await event.delete()

@register(outgoing=True, pattern="^.insult$")
@errors_handler
async def insult(e):
    """ I make you cry !! """
    if not e.text[0].isalpha() and e.text[0] in ("."):
        await e.edit(random.choice(INSULT_STRINGS))

@register(outgoing=True, pattern="^.vapor(?: |$)(.*)")
@errors_handler
async def vapor(vpr):
    """ Vaporize everything! """
    if not vpr.text[0].isalpha() and vpr.text[0] in ("."):
        reply_text = list()
        textx = await vpr.get_reply_message()
        message = vpr.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await vpr.edit("`Ｇｉｖｅ ｓｏｍｅ ｔｅｘｔ ｆｏｒ ｖａｐｏｒ！`")
            return

        for charac in message:
            if 0x21 <= ord(charac) <= 0x7F:
                reply_text.append(chr(ord(charac) + 0xFEE0))
            elif ord(charac) == 0x20:
                reply_text.append(chr(0x3000))
            else:
                reply_text.append(charac)

        await vpr.edit("".join(reply_text))

@register(outgoing=True, pattern="^.str(?: |$)(.*)")
@errors_handler
async def stretch(stret):
    """ Stretch it."""
    if not stret.text[0].isalpha() and stret.text[0] in ("."):
        textx = await stret.get_reply_message()
        message = stret.text
        message = stret.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await stret.edit("`GiiiiiiiB sooooooomeeeeeee teeeeeeext!`")
            return

        count = random.randint(3, 10)
        reply_text = re.sub(r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])",
                            (r"\1" * count), message)
        await stret.edit(reply_text)

@register(outgoing=True, pattern="^.zal(?: |$)(.*)")
@errors_handler
async def zal(zgfy):
    """ Invoke the feeling of chaos. """
    if not zgfy.text[0].isalpha() and zgfy.text[0] in ("."):
        reply_text = list()
        textx = await zgfy.get_reply_message()
        message = zgfy.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await zgfy.edit(
                "`gͫ ̆ i̛ ̺ v͇̆ ȅͅ   a̢ͦ   s̴̪ c̸̢ ä̸ rͩͣ y͖͞   t̨͚ é̠ x̢͖  t͔͛`"
            )
            return

        for charac in message:
            if not charac.isalpha():
                reply_text.append(charac)
                continue

            for _ in range(0, 3):
                randint = random.randint(0, 2)

                if randint == 0:
                    charac = charac.strip() + \
                        random.choice(ZALG_LIST[0]).strip()
                elif randint == 1:
                    charac = charac.strip() + \
                        random.choice(ZALG_LIST[1]).strip()
                else:
                    charac = charac.strip() + \
                        random.choice(ZALG_LIST[2]).strip()

            reply_text.append(charac)

        await zgfy.edit("".join(reply_text))

@register(outgoing=True, pattern="^.hi$")
@errors_handler
async def hoi(hello):
    """ Greet everyone! """
    if not hello.text[0].isalpha() and hello.text[0] in ("."):
        await hello.edit(random.choice(HELLOSTR))

@register(outgoing=True, pattern="^.clock$")
@errors_handler
async def _(event):
    if not event.text[0].isalpha() and event.text[0] in ("."):
        if event.fwd_from:
            return
        deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
        try:
            for _ in range(32):
                await asyncio.sleep(0.1)
                await event.edit("".join(deq))
                deq.rotate(1)
        except BaseException:
            return

@register(outgoing=True, pattern="^.mock(?: |$)(.*)")
@errors_handler
async def spongemocktext(mock):
    """ Do it and find the real fun. """
    if not mock.text[0].isalpha() and mock.text[0] in ("."):
        reply_text = list()
        textx = await mock.get_reply_message()
        message = mock.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await mock.edit("`gIvE sOMEtHInG tO MoCk!`")
            return

        for charac in message:
            if charac.isalpha() and random.randint(0, 1):
                to_app = charac.upper() if charac.islower() else charac.lower()
                reply_text.append(to_app)
            else:
                reply_text.append(charac)

        await mock.edit("".join(reply_text))

@register(outgoing=True, pattern="^.clap(?: |$)(.*)")
@errors_handler
async def claptext(memereview):
    """ Praise people! """
    if not memereview.text[0].isalpha() and memereview.text[0] in (
            "."):
        textx = await memereview.get_reply_message()
        message = memereview.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await memereview.edit("`Hah, I don't clap pointlessly!`")
            return
        reply_text = "👏 "
        reply_text += message.replace(" ", " 👏 ")
        reply_text += " 👏"
        await memereview.edit(reply_text)

@register(outgoing=True, pattern="^.bt$")
@errors_handler
async def bluetext(bt_e):
    """ Believe me, you will find this useful. """
    if not bt_e.text[0].isalpha() and bt_e.text[0] in ("."):
        if await bt_e.get_reply_message():
            await bt_e.edit(
                "/BLUETEXT /MUST /CLICK.\n"
                "/ARE /YOU /A /STUPID /ANIMAL /WHICH /IS /ATTRACTED /TO /COLOURS ?"
            )

@register(outgoing=True, pattern="^.lfy (.*)")
@errors_handler
async def let_me_google_that_for_you(lmgtfy_q):
    if not lmgtfy_q.text[0].isalpha() and lmgtfy_q.text[0] in ("."):
        textx = await lmgtfy_q.get_reply_message()
        qry = lmgtfy_q.pattern_match.group(1)
        if qry:
            query = str(qry)
        elif textx:
            query = textx
            query = query.message
        query_encoded = query.replace(" ", "+")
        lfy_url = f"http://lmgtfy.com/?s=g&iie=1&q={query_encoded}"
        payload = {'format': 'json', 'url': lfy_url}
        r = requests.get('http://is.gd/create.php', params=payload)
        await lmgtfy_q.edit(f"[{query}]({r.json()['shorturl']})")

@register(pattern=r".scam(?: |$)(.*)", outgoing=True)
@errors_handler
async def scam(event):
    """ Just a small command to fake chat actions for fun !! """
    if not event.text[0].isalpha() and event.text[0] in ("."):
        options = [
            'typing', 'contact', 'game', 'location', 'voice', 'round', 'video',
            'photo', 'document', 'cancel'
        ]
        input_str = event.pattern_match.group(1)
        args = input_str.split()
        if len(args) is 0:  # Let bot decide action and time
            scam_action = random.choice(options)
            scam_time = random.randint(30, 60)
        elif len(args) is 1:  # User decides time/action
            try:
                scam_action = str(args[0]).lower()
                scam_time = random.randint(30, 60)
            except ValueError:
                scam_action = random.choice(options)
                scam_time = int(args[0])
        elif len(args) is 2:  # User decides both action and time
            scam_action = str(args[0]).lower()
            scam_time = int(args[1])
        else:
            await event.edit("`Invalid Syntax !!`")
            return
        try:
            if (scam_time > 0):
                await event.delete()
                async with event.client.action(event.chat_id, scam_action):
                    await asyncio.sleep(scam_time)
        except BaseException:
            return

@register(pattern=r".type(?: |$)(.*)", outgoing=True)
@errors_handler
async def typewriter(typew):
    """ Just a small command to make your keyboard become a typewriter! """
    if not typew.text[0].isalpha() and typew.text[0] in ("."):
        textx = await typew.get_reply_message()
        message = typew.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await typew.edit("`Give a text to type!`")
            return
        sleep_time = 0.03
        typing_symbol = "█"
        old_text = ""
        await typew.edit(typing_symbol)
        await asyncio.sleep(sleep_time)
        for character in message:
            old_text = old_text + "" + character
            typing_text = old_text + "" + typing_symbol
            await typew.edit(typing_text)
            await asyncio.sleep(sleep_time)
            await typew.edit(old_text)
            await asyncio.sleep(sleep_time)

CMD_HELP.update({
    "memes":
    ".vapor\
\nUsage: Vaporize everything!\
\n\n.str\
\nUsage: Stretch it.\
\n\n.zal\
\nUsage: Invoke the feeling of chaos.\
\n\n.clock\
\nUsage: kensar clock animation.\
\n\n.hi\
\nUsage: Greet everyone!\
\n\n.coinflip <heads/tails>\
\nUsage: Flip a coin !!\
\n\n.slap\
\nUsage: reply to slap them with random objects !!\
\n\n.mock\
\nUsage: Do it and find the real fun.\
\n\n.clap\
\nUsage: Praise people!\
\n\n.bt\
\nUsage: Believe me, you will find this useful.\
\n\n.type\
\nUsage: Just a small command to make your keyboard become a typewriter!\
\n\n.lfy <query>\
\nUsage: Let me Google that for you real quick !!\
\n\n.decide [Optional: (yes, no, maybe)]\
\nUsage: Make a quick decision.\
\n\n.scam <action> <time>\
\n[Available Actions: (typing, contact, game, location, voice, round, video, photo, document, cancel)]\
\nUsage: Create fake chat actions, for fun. (Default action: typing)\
\n\n\nThanks to 🅱️ottom🅱️ext🅱️ot (@NotAMemeBot) for some of these."
})
