import os
from distutils.util import strtobool as sb
from logging import basicConfig, getLogger, INFO, DEBUG
from sys import version_info

import pylast
from dotenv import load_dotenv
from requests import get
from telethon import TelegramClient
from telethon.sessions import StringSession

load_dotenv("config.env")

CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))  # Bot Logs setup

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
    API_KEY = os.environ.get("API_KEY", None)  # tg API key
    API_HASH = os.environ.get("API_HASH", None)  # tg API hash
    STRING_SESSION = os.environ.get("STRING_SESSION", None)  # Userbot Session String
    BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", "0"))  # Logging channel/group ID
    BOTLOG = sb(os.environ.get("BOTLOG", "False"))  # Logging channel/group configuration.
    CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))  # Console verbose logging
    ALIVE_NAME = os.environ.get("ALIVE_NAME", None)  # Default .alive name
    OWNER_ID = int(os.environ.get("OWNER_ID", 0))
    CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME", "True"))
    HOMIES = []
    GIRLFRIEND = None
    GBANS = os.environ.get("GBANS", False)
    GBAN_BOTS = os.environ.get("GBAN_BOTS", None)
    LANG = os.environ.get("LANG", 'en')
    AUTOMATION_ENABLED = False
    AUTOMATION_SENDERS = []
    AUTOMATION_COMMANDS = []
    AUTOMATION_TRIGGERS = []
    Q_API_TOKEN = os.environ.get("Q_API_TOKEN", None)  # Quotly API key http://antiddos.systems
    OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)
    OPEN_WEATHER_MAP_DEFCITY = os.environ.get("OPEN_WEATHER_MAP_DEFCITY", None)
    UPSTREAM_REPO_URL = os.environ.get("UPSTREAM_REPO_URL",
                                       "https://github.com/nunopenim/tguserbot.git")  # Custom (forked) repo URL for updater.

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
    GIRLFRIEND = Config.GIRLFRIEND
    OWNER_ID = Config.OWNER_ID
    GBANS = Config.GBANS
    GBAN_BOTS = Config.GBAN_BOTS
    AUTOMATION_ENABLED = Config.AUTOMATION_ENABLED
    AUTOMATION_SENDERS = Config.AUTOMATION_SENDERS
    AUTOMATION_COMMANDS = Config.AUTOMATION_COMMANDS
    AUTOMATION_TRIGGERS = Config.AUTOMATION_TRIGGERS
    Q_API_TOKEN = Config.Q_API_TOKEN  # Quotly API key http://antiddos.systems
    OPEN_WEATHER_MAP_APPID = Config.OPEN_WEATHER_MAP_APPID
    OPEN_WEATHER_MAP_DEFCITY = Config.OPEN_WEATHER_MAP_DEFCITY
    UPSTREAM_REPO_URL = Config.UPSTREAM_REPO_URL  # Custom (forked) repo URL for updater.

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
VERSION = "2.0.0-alpha"
