import asyncio
import random
import re
import time

import requests
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from tg_userbot import CMD_HELP
from tg_userbot.events import register

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
    " ", ],
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
        " ͡", ]]

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
    "🚰"]

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
    "You got your head so far up your ass, you can chew food twice."]

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
    "Hiya!"]

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
    "ties {victim} to a chair and {throws} **{item}** at them. {emoji}"]

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
    "a Big-Mac")

THROW = [
    "throws",
    "flings",
    "chucks",
    "hurls"]

HIT = [
    "hits",
    "whacks",
    "slaps",
    "smacks",
    "spanks",
    "bashes"]

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
    "\U0001F632")

PUNCH_TEMPLATES = [
    "{punches} {victim} to assert dominance.",
    "{punches} {victim} to see if they shut the fuck up for once.",
    "{punches} {victim} because they were asking for it.",
    "It's over {victim}, they have the high ground.",
    "performs a superman punch on {victim}, {victim} is rekt now.",
    "makes {victim} go on tiktok. {victim} gets cancer. ",
    "kills off {victim} with a T.K.O",
    "attacks {victim} with a billiard cue. A bloody mess.",
    "disintegrates {victim} with a MG.",
    "A hit and run over {victim} performed by me",
    "punches {victim} into the throat. Warning, choking hazard!",
    "drops a piano on top of {victim}. A harmonical death.",
    "throws rocks at {victim}",
    "forces {victim} to drink chlorox. What a painful death.",
    "got sliced in half by {victim}'s katana.",
    "makes {victim} fall on their sword. A stabby death lol.",
    "kangs {victim} 's life energy away.",
    "shoots {victim} into a million pieces. Hasta la vista baby.",
    "drops the fridge on {victim}. Beware of crushing.",
    "engages a guerilla tactic on {victim}",
    "ignites {victim} into flames. IT'S LIT FAM.",
    "pulls a loaded 12 gauge on {victim}.",
    "throws a Galaxy Note7 into {victim}'s general direction. A bombing massacre.",
    "walks with {victim} to the end of the world, then pushes him over the edge.",
    "performs a Stabby McStabby on {victim} with a butterfly.",
    "cuts {victim}'s neck off with a machete. A blood bath.",
    "secretly fills in {victim}'s cup with Belle Delphine's Gamer Girl Bathwater instead of water. Highly contagious herpes.",
    "is tea cupping on {victim} after a 1v1, to assert their dominance.",
    "asks for {victim}'s last words. {victim} is ded now.",
    "lets {victim} know their position.",
    "makes {victim} to his slave. What is your bidding? My Master.",
    "forces {victim} to commit suicide.",
    "shouts 'it's garbage day' at {victim}.",
    "throws his axe at {victim}.",
    "is now {victim}'s grim reaper.",
    "slappety slap's {victim}.",
    "ends the party.",
    "will never know what hit them.",
    "breaks {victim}'s neck like a kitkat.",
    "flings knives at {victim}.",
    "gangs {victim} in a drive by.",
    "Thanks to my airstrike, {victim} is no more.",
    "waterboard's {victim}.",
    "hangs {victim} upside down.",
    "breaks (victim)'s skull with a PS4.",
    "throws Xbox controller batteries at {victim}'s face.",
    "shouts 'Look at me, I'm the Captain now.' at {victim}.",
    "puts {victim} in their place.",
    "poisons {victim}'s meal, it was their last meal.",
    "burns {victim} into ashes.",
    "bites in the dust.",
    "stabs {victim} in their back, what a way to die.",
    "uses {victim} to play Fruit Ninja.",
    "blueballs {victim}.",
    "makes the fool die a fool's death.",
    "orders Agent 47 on {victim}'s ass.",
    "gets struck by a lightning. Warning, high tension.",
    "breaks all of {victim}'s bones.",
    "Someone save {victim} because I is about to murder them.",
    "throws {victim} into a volcano.",
    "chokes {victim} through the force.",
    "throws their lightsaber at {victim}.",
    "orders a full broadside on {victim}.",
    "deploys the garrison on {victim}.",
    "lets freeze {victim} to death.",
    "throws {victim} across the room by the force.",
    "makes {victim} go crazy by high pitch sounds.",
    "rolls over {victim} with a Panzerkampfwagen VI Tiger.",
    "blows {victim} up with a bazooka.",
    "plays Sniper Elite with {victim} as the target.",
    "yeets {victim}'s ass.)",
    "puts a grenade in {victim}'s hood.",
    "throws an iPhone 11 Pro Max at {victim}'s face.",
    "throws a Galaxy S20 Ultra 5G at {victim}'s face.",
    "draws a dick on {victim}'s forehead.",
    "cuts open {victim}'s throat. Very bloody.",
    "shoots {victim} to dust with a {gun}.",
    "lands a headshot on {victim} with their {gun}.",
    "shoots down {victim} with a {gun}."
    "stashes a Glock."
    "lures {victim} on a minefield.",
    "wins over {victim} in a western 1v1.",
    "plays robbers and gendarmes with {victim}.",
    "tries their new {gun} on {victim}.",
    "steals all of {victim}'s money. Now they're broke af.",
    "drops a TV on {victim}.",
    "throws their Apple TV at {victim}.",
    "hijacks {victim}'s ship.",
    "makes {victim} sign their death certificate.",
    "kangs everything what {victim} owns.",
    "manipulates {victim}'s breaks.",
    "ties {victim} down on the train tracks.",
    "chops {victim}'s arm off with their lightsaber.",
]

PUNCH = [
    "punches",
    "RKOs",
    "smashes the skull of",
    "throws a pipe wrench at",
]
GUN = [
    "AK-47",
    "M1911",
    "M1928 Thommy",
    "M1 Abrams tank",
    "M16",
    "M1 Garand",
    "Avtomat Federov",
    "CHAUCHAT",
    "Avtomat Kalashnikov",
    "M1928.A1 Thompson",
    "M1911.A1",
    ".45 ACP",
    "Colt 1911",
    "Ithaca 1911",
    "9mm Luger",
    "UZI",
    "Galil Ace",
    "StG 44",
    "MP 38",
    "MP 40",
    "StG 40",
    "Model 27",
    ".44 Magnum",
    "MP 28",
    "M8 con Tromboncino",
    "STEN",
    "M3 Carbine",
    "M3 Grease Gun",
    "M2 Carbine",
    "Kar98k",
    "Maschinengewehr 34",
    "Maschinengewehr 42",
    "HK MP5",
    "MP5",
    "Heckler & Koch G36 C",
    "Heckler & Koch G36",
    "HK G36 C",
    "HK G36",
    "SCAR FN",
    "Glock 17",
    "Glock 18",
    "Glock 19",
    "Glock 20",
    "Glock 21",
    "Glock 22",
    "Glock 23",
    "Glock 30",
    "Glock 40",
    "Glock 42",
    "Glock 44",
    "Glock 45",
    "Glock 48",
    "M1941 Johnson Rifle",
    "M1941 Johnson",
    "Nambu Type 2A",
    "Type 100",
    "FLAK",
    "Type 99 Arisaka",
    "Ribeyrolles 1918",
    "Panzerbüchse 39"
    "Panzerbüchse Boys",
    "M1897",
    "12 Gauge Automatic",
    "Drilling M30",
    "PPsh",
    "Sturmgewehr 40",
    "Sturmgewehr 44",
    "Maschinenpistole 38",
    "Maschinenpistole 40",
    "AK-44S",
    "Colt 44 Magnum",
    "AA-12",
    "ACR",
    "Desert Eagle",
    ".50",
    "FAL",
    "M-200 Intervention",
    "M249 Saw",
    "M4A1",
    "FN P90",
    "Suomi KP31",
    "PDR",
    "PPsh-41",
    "SPAS-12",
    "Beretta M9",
    "SCAR-H",
    "Thompson M1921",
    "M1921",
    "HK USP",
    "Heckler & Koch USP",
    "XD-9",
    "1887 Mare S Leg",
    "M1912 Repetierpistole",
    "Ruby",
    "AK-45 Korovin",
    "AK-45 KOROVIN",
    "AVTOMAT KALASHNIKOV 45 KOROVIN",
    "AK-74",
    "Avtomat Kalashnikov 74",
    "Avtomat Kalashnikov 47",
    "AR-70",
    "Fliegerfaust",
    "PIAT",
    "M1A1 Bazooka",
    "Bazooka",
    "Bangalore",
    "AK-5C",
    "Avtomat Kalashnikov 5C",
    "Ameli",
    "Welgun",
    "Coach Gun",
    "HK 417",
    "Heckler & Koch 417",
    "Honey Badger",
    "Sjögren",
    "M1898",
    "Krag-Jørgensen",
    "Krag-Jørgensen M1898",
    "Maschinengewehr 15",
    "MG 15",
    "Madsen MG",
    "Panzerfaust",
    "PANZERFAUST",
    "PANZERABWEHRMINE",
    "Panzerabwehrmine",
    "SCAR PDW",
    "XD59",
    "Model 37 shotgun",]
    

@register(outgoing=True, pattern=r"^.coinflip$")
async def coin(event):  # coinflip
    if not event.text[0].isalpha() and event.text[0] in ("."):
        r = random.randint(1, 10000)
        await event.edit("`Throwing the coin...`")
        time.sleep(3)
        if r % 2 == 1:
            await event.edit("`The coin landed on: Heads`")
        elif r % 2 == 0:
            await event.edit("`The coin landed on: Tails`")
        else:
            await event.edit("`Mate, this is a beer bottle cap, give me a coin!`")

@register(pattern="^.punch(?: |$)(.*)", outgoing=True)
async def who(event): #punch
    if not event.text[0].isalpha() and event.text[0] in ("."):
        if event.fwd_from:
            return
        replied_user = await get_user(event)
        caption = await punch(replied_user, event)
        message_id_to_reply = event.message.reply_to_msg_id
        if not message_id_to_reply:
            message_id_to_reply = None
        try:
            await event.edit(caption)
        except BaseException:
            await event.edit("`Can't punch this person, loading 12 gauge buckshot in my shotgun!!`")

async def punch(replied_user, event):  # builds the punch msg itself
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    username = replied_user.user.username
    if username:
        punched = "@{}".format(username)
    else:
        punched = f"[{first_name}](tg://user?id={user_id})"
    temp = random.choice(PUNCH_TEMPLATES)
    item = random.choice(ITEMS)
    hit = random.choice(HIT)
    throw = random.choice(THROW)
    emoji = random.choice(EMOJI)
    gun = random.choice(GUN)
    caption = "..." + temp.format(victim=punched, item=item, hits=hit, gun=gun, throws=throw, emoji=emoji)
    return caption
            

@register(pattern="^.slap(?: |$)(.*)", outgoing=True)
async def who(event):  # slap
    if not event.text[0].isalpha() and event.text[0] in ("."):
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
            await event.edit("`Can't slap this person, loading 12 gauge buckshot in my shotgun!!`")


async def get_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            self_user = await event.client.get_me()
            user = self_user.id
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(GetFullUserRequest(user_object.id))
        except (TypeError, ValueError):
            await event.edit("`This dude doesn't even exist`")
            return None
    return replied_user


async def slap(replied_user, event):  # builds the slap msg itself
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
    caption = "..." + temp.format(victim=slapped, item=item, hits=hit, throws=throw, emoji=emoji)
    return caption


@register(outgoing=True, pattern="^.decide(?: |$)(.*)")
async def decide(event):  # yes/no
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
                r = requests.get(f"https://yesno.wtf/api?force={message.lower()}").json()
            except BaseException:
                await event.edit("`Available decisions:` *yes*, *no*, *maybe*")
                return
        await event.client.send_message(event.chat_id, str(r["answer"]).upper(), reply_to=message_id, file=r["image"])
        await event.delete()


@register(outgoing=True, pattern="^.insult$")
async def insult(e):  # insult from insult structure
    if not e.text[0].isalpha() and e.text[0] in ("."):
        await e.edit(random.choice(INSULT_STRINGS))


@register(outgoing=True, pattern="^.vapor(?: |$)(.*)")
async def vapor(vpr):  # vapor
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
async def stretch(stret):  # stretch
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
        reply_text = re.sub(r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])", (r"\1" * count), message)
        await stret.edit(reply_text)


@register(outgoing=True, pattern="^.zal(?: |$)(.*)")
async def zal(zgfy):  # chaotic
    if not zgfy.text[0].isalpha() and zgfy.text[0] in ("."):
        reply_text = list()
        textx = await zgfy.get_reply_message()
        message = zgfy.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await zgfy.edit("`gͫ ̆ i̛ ̺ v͇̆ ȅͅ   a̢ͦ   s̴̪ c̸̢ ä̸ rͩͣ y͖͞   t̨͚ é̠ x̢͖  t͔͛`")
            return
        for charac in message:
            if not charac.isalpha():
                reply_text.append(charac)
                continue
            for _ in range(0, 3):
                randint = random.randint(0, 2)
                if randint == 0:
                    charac = charac.strip() + random.choice(ZALG_LIST[0]).strip()
                elif randint == 1:
                    charac = charac.strip() + random.choice(ZALG_LIST[1]).strip()
                else:
                    charac = charac.strip() + random.choice(ZALG_LIST[2]).strip()
            reply_text.append(charac)
        await zgfy.edit("".join(reply_text))


@register(outgoing=True, pattern="^.hi$")
async def hoi(hello):  # hi
    if not hello.text[0].isalpha() and hello.text[0] in ("."):
        await hello.edit(random.choice(HELLOSTR))


@register(outgoing=True, pattern="^.oof$")
async def Oof(e):
    if not e.text[0].isalpha() and e.text[0] in ("."):
        t = "Oof"
        for j in range(15):
            t = t[:-1] + "of"
            await e.edit(t)


@register(outgoing=True, pattern="^.mock(?: |$)(.*)")
async def spongemocktext(mock):
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
async def claptext(memereview):  # clap
    if not memereview.text[0].isalpha() and memereview.text[0] in ("."):
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
async def bluetext(bt_e):
    if not bt_e.text[0].isalpha() and bt_e.text[0] in ("."):
        if await bt_e.get_reply_message() and bt_e.is_group:
            await bt_e.edit(
                "/BLUE /TEXT /MUST /CLICK\n"
                "/ARE /YOU /A /STUPID /COW /WHICH /IS /ATTRACTED /TO /COLORS ?"
            )


@register(outgoing=True, pattern=r"^.f (.*)")
async def payf(event):
    if not event.text[0].isalpha() and event.text[0] in ("."):
        paytext = event.pattern_match.group(1)
        pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
            paytext * 8, paytext * 8, paytext * 2, paytext * 2, paytext * 2,
            paytext * 6, paytext * 6, paytext * 2, paytext * 2, paytext * 2,
            paytext * 2, paytext * 2)
        await event.edit(pay)


@register(outgoing=True, pattern="^.lfy (.*)")
async def let_me_google_that_for_you(lmgtfy_q):  # img.gtfy
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
async def scam(event):
    if not event.text[0].isalpha() and event.text[0] in ("."):
        options = [
            'typing', 'contact', 'game', 'location', 'voice', 'round', 'video',
            'photo', 'document', 'cancel']
        input_str = event.pattern_match.group(1)
        args = input_str.split()
        if len(args) == 0:  # Let bot decide action and time
            scam_action = random.choice(options)
            scam_time = random.randint(30, 60)
        elif len(args) == 1:  # User decides time/action
            try:
                scam_action = str(args[0]).lower()
                scam_time = random.randint(30, 60)
            except ValueError:
                scam_action = random.choice(options)
                scam_time = int(args[0])
        elif len(args) == 2:  # User decides both action and time
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
async def typewriter(typew):
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
        sleep_time = 0.1
        typing_symbol = "|"
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


@register(outgoing=True, pattern="^.gei$")
async def isgei(gei):
    if not gei.text[0].isalpha() and gei.text[0] in ("."):
        if await gei.get_reply_message() and gei.is_group or gei.to_id:
            await gei.edit("`┈┈┈╭━━━━━╮┈┈┈┈┈\n"
                           "┈┈┈┃┊┊┊┊┊┃┈┈┈┈┈\n"
                           "┈┈┈┃┊┊╭━╮┻╮┈┈┈┈\n"
                           "┈┈┈╱╲┊┃▋┃▋┃┈┈┈┈\n"
                           "┈┈╭┻┊┊╰━┻━╮┈┈┈┈\n"
                           "┈┈╰┳┊╭━━━┳╯┈┈┈┈\n"
                           "┈┈┈┃┊┃╰━━┫┈NIGGA U GEY\n"
                           "┈┈┈┈┈┈┏━┓┈┈┈┈┈┈`")


@register(outgoing=True, pattern="^.nou$")
async def isgei(gei):
    if not gei.text[0].isalpha() and gei.text[0] in ("."):
        if await gei.get_reply_message() and gei.is_group or gei.to_id:
            await gei.edit("`┈╭╮╭╮\n"
                           "┈┃┃┃┃\n"
                           "╭┻┗┻┗╮\n"
                           "┃┈▋┈▋┃\n"
                           "┃┈╭▋━╮━╮\n"
                           "┃┈┈╭╰╯╰╯╮\n"
                           "┫┈┈  NoU\n"
                           "┃┈╰╰━━━━╯\n"
                           "┗━━┻━┛`")


@register(outgoing=True, pattern=r"^.caps(?: |$)([\s\S]*)")
async def to_upper(request):
    if not request.text[0].isalpha() and request.text[0] in ("."):
        textx = await request.get_reply_message()
        message = request.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await request.edit("`Usage: .caps <text>`")
            return
        reply = ''
        reply += message.upper()
        await request.edit(reply)


@register(outgoing=True, pattern=r"^.small(?: |$)([\s\S]*)")
async def to_lower(request):
    if not request.text[0].isalpha() and request.text[0] in ("."):
        textx = await request.get_reply_message()
        message = request.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await request.edit("`Usage: .small <text>`")
            return
        reply = ''
        reply += message.lower()
        await request.edit(reply)


@register(outgoing=True, pattern=r"^.noformat(?: |$)([\s\S]*)")
async def noformat(request):
    if not request.text[0].isalpha() and request.text[0] in ("."):
        textx = await request.get_reply_message()
        message = request.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await request.edit("`Usage: .noformat <text>/<reply>`")
            return
        reply = ''
        reply += '```' + message + '```'
        await request.edit(reply)


CMD_HELP.update({
    "memes":
        ".vapor\
    \nUsage: Vaporize everything!\
    \n\n.str\
    \nUsage: Stretch it.\
    \n\n.zal\
    \nUsage: Invoke the feeling of chaos.\
    \n\n.oof\
    \nUsage: Ooooof\
    \n\n.caps <text>\
    \nUsage: Converts text to uppercase.\
    \n\n.small <text>\
    \nUsage: Converts text to uppercase.\
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
    \n\n.f <emoji/character>\
    \nUsage: Pay Respects.\
    \n\n.bt\
    \nUsage: Believe me, you will find this useful.\
    \n\n.punch\
    \nUsage: show who's boss\
    \n\n.noformat\
    \nUsage: Returns text without formatting.\
    \n\n.gei\
    \nUsage: Use this as a reply if your friend does something gei.\
    \n\n.nou\
    \nUsage: Return whatever someone said to themself.\
    \n\n.type\
    \nUsage: Just a small command to make your keyboard become a typewriter!\
    \n\n.lfy <query>\
    \nUsage: Let me Google that for you real quick !!\
    \n\n.decide [Optional: (yes, no, maybe)]\
    \nUsage: Make a quick decision.\
    \n\n.scam <action> <time>\
    \n[Available Actions: (typing, contact, game, location, voice, round, video, photo, document, cancel)]\
    \nUsage: Create fake chat actions, for fun. (Default action: typing)\
    \n\n\nThanks to 🅱️ottom🅱️ext🅱️ot (@NotAMemeBot) for some of these."})
