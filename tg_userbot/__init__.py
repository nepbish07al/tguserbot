import os
import pylast
from sys import version_info
from logging import basicConfig, getLogger, INFO, DEBUG
from distutils.util import strtobool as sb
from dotenv import load_dotenv
from requests import get
from telethon import TelegramClient
from telethon.sessions import StringSession

load_dotenv("config.env")

CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False")) # Bot Logs setup

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=DEBUG)
else:
    basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=INFO)
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 6:
    LOGS.error("You MUST have a python version of at least 3.6."
               "Multiple features depend on this. Bot quitting.")
    quit(1)

ENV = bool(os.environ.get('ENV', False))

if ENV:
    API_KEY = os.environ.get("API_KEY", None) #tg API key
    API_HASH = os.environ.get("API_HASH", None) #tg API hash
    STRING_SESSION = os.environ.get("STRING_SESSION", None) # Userbot Session String
    BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", "0")) # Logging channel/group ID
    BOTLOG = sb(os.environ.get("BOTLOG", "False")) # Logging channel/group configuration.
    CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False")) # Console verbose logging
    ALIVE_NAME = os.environ.get("ALIVE_NAME", None) # Default .alive name
    CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME", "True"))
    HOMIES = []
    LANG = os.environ.get("LANG", 'en')

else:
# importing separate config to be able to keep our shit hidden
    from tg_userbot.config import Development as Config
    API_KEY = Config.API_KEY
    API_HASH = Config.API_HASH
    if not API_KEY:
        import sys
        print("Your API_KEY is not defined", file=sys.stderr)
        quit(1)
    if not API_HASH:
        import sys
        print("Your API_HASH is not defined", file=sys.stderr)
        quit(1)
    STRING_SESSION = Config.STRING_SESSION
    BOTLOG_CHATID = int(Config.BOTLOG_CHATID)
    BOTLOG = Config.BOTLOG
    CONSOLE_LOGGER_VERBOSE = Config.CONSOLE_LOGGER_VERBOSE
    ALIVE_NAME = Config.ALIVE_NAME
    CLEAN_WELCOME = Config.CLEAN_WELCOME
    HOMIES = Config.HOMIES
    LANG = Config.LANG

TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./downloads")

# 'bot' variable
if STRING_SESSION:
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    bot = TelegramClient("userbot", API_KEY, API_HASH)

# Global Variables
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
ENABLE_KILLME = True
CMD_HELP = {}
VERSION = "1.1.0"
