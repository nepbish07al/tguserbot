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

    # Bleep Blop, this is a bot ;)
    PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN", "False"))

    # Console verbose logging
    CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

    # SQL Database URI
    DB_URI = os.environ.get("DATABASE_URL", None)

    # OCR API key
    OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", None)

    # remove.bg API key
    REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)

    # Chrome Driver and Headless Google Chrome Binaries
    CHROME_DRIVER = os.environ.get("CHROME_DRIVER", None)
    GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN", None)

    # OpenWeatherMap API Key
    OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)

    # Anti Spambot Config
    ANTI_SPAMBOT = sb(os.environ.get("ANTI_SPAMBOT", "False"))

    ANTI_SPAMBOT_SHOUT = sb(os.environ.get("ANTI_SPAMBOT_SHOUT", "False"))

    # Youtube API key
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", None)

    # Default .alive name
    ALIVE_NAME = os.environ.get("ALIVE_NAME", None)

    # Time & Date - Country and Time Zone
    COUNTRY = str(os.environ.get("COUNTRY", ""))

    TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))

    # Clean Welcome
    CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME", "True"))

    # Last.fm Module
    BIO_PREFIX = os.environ.get("BIO_PREFIX", None)
    DEFAULT_BIO = os.environ.get("DEFAULT_BIO", None)

    LASTFM_API = os.environ.get("LASTFM_API", None)
    LASTFM_SECRET = os.environ.get("LASTFM_SECRET", None)
    LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME", None)
    LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD", None)
    LASTFM_PASS = pylast.md5(LASTFM_PASSWORD_PLAIN)
    # Google Drive Module
    G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
    G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
    G_DRIVE_AUTH_TOKEN_DATA = os.environ.get("G_DRIVE_AUTH_TOKEN_DATA", None)
    GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", None)
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
    DB_URI = Config.DB_URI
    OCR_SPACE_API_KEY = Config.OCR_SPACE_API_KEY
    REM_BG_API_KEY = Config.REM_BG_API_KEY
    CHROME_DRIVER = Config.CHROME_DRIVER
    GOOGLE_CHROME_BIN = Config.GOOGLE_CHROME_BIN
    OPEN_WEATHER_MAP_APPID = Config.OPEN_WEATHER_MAP_APPID
    ANTI_SPAMBOT = Config.ANTI_SPAMBOT
    ANTI_SPAMBOT_SHOUT = Config.ANTI_SPAMBOT_SHOUT
    YOUTUBE_API_KEY = Config.YOUTUBE_API_KEY
    ALIVE_NAME = Config.ALIVE_NAME
    COUNTRY = str(Config.COUNTRY)
    TZ_NUMBER = int(Config.TZ_NUMBER)
    CLEAN_WELCOME = Config.CLEAN_WELCOME
    BIO_PREFIX = Config.BIO_PREFIX
    DEFAULT_BIO = Config.DEFAULT_BIO
    LASTFM_API = Config.LASTFM_API
    LASTFM_SECRET = Config.LASTFM_SECRET
    LASTFM_USERNAME = Config.LASTFM_USERNAME
    LASTFM_PASSWORD_PLAIN = Config.LASTFM_PASSWORD_PLAIN
    LASTFM_PASS = pylast.md5(LASTFM_PASSWORD_PLAIN)
    G_DRIVE_CLIENT_ID = Config.G_DRIVE_CLIENT_ID
    G_DRIVE_CLIENT_SECRET = Config.G_DRIVE_CLIENT_SECRET
    G_DRIVE_AUTH_TOKEN_DATA = Config.G_DRIVE_AUTH_TOKEN_DATA
    GDRIVE_FOLDER_ID = Config.GDRIVE_FOLDER_ID


if not LASTFM_USERNAME == "None":
    lastfm = pylast.LastFMNetwork(api_key=LASTFM_API,
                                  api_secret=LASTFM_SECRET,
                                  username=LASTFM_USERNAME,
                                  password_hash=LASTFM_PASS)
else:
    lastfm = None
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
