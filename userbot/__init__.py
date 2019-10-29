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

# Bot Logs setup:
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                level=INFO)
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 6:
    LOGS.error("You MUST have a python version of at least 3.6."
               "Multiple features depend on this. Bot quitting.")
    quit(1)

ENV = bool(os.environ.get('ENV', False))

if ENV:
    # Telegram App KEY and HASH
    API_KEY = os.environ.get("API_KEY", None)
    API_HASH = os.environ.get("API_HASH", None)
    # Userbot Session String
    STRING_SESSION = os.environ.get("STRING_SESSION", None)
    # Logging channel/group configuration.
    BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", "0"))
    BOTLOG = sb(os.environ.get("BOTLOG", "False"))
    # Console verbose logging
    CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))
    # Default .alive name
    ALIVE_NAME = os.environ.get("ALIVE_NAME", None)
    # Time & Date - Country and Time Zone
    COUNTRY = str(os.environ.get("COUNTRY", ""))
    TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))
    # Clean Welcome
    CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME", "True"))
else:
# importing separate config to be able to keep our shit hidden
    from userbot.config import Development as Config
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
    PM_AUTO_BAN = Config.PM_AUTO_BAN
    CONSOLE_LOGGER_VERBOSE = Config.CONSOLE_LOGGER_VERBOSE
    ALIVE_NAME = Config.ALIVE_NAME
    COUNTRY = str(Config.COUNTRY)
    TZ_NUMBER = int(Config.TZ_NUMBER)
    CLEAN_WELCOME = Config.CLEAN_WELCOME

TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY",
                                         "./downloads")

# 'bot' variable
if STRING_SESSION:
    # pylint: disable=invalid-name
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    # pylint: disable=invalid-name
    bot = TelegramClient("userbot", API_KEY, API_HASH)

# Global Variables
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
ENABLE_KILLME = True
CMD_HELP = {}
ISAFK = False
AFKREASON = None
