# Copyright (C) 2019 Corsicanu.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

if not __name__.endswith("sample_config"):
    import sys
    print("Extend this sample config to a config file, don't just rename and change values here. Doing that WILL backfire on you.\nBot quitting.", file=sys.stderr)
    quit(1)

# Create a new config.py file in same dir and import, then extend this class.
class Config(object):
    OWNER_ID = None # required OWNER ID
    API_KEY = None # required tg Key
    API_HASH = None # required tg hash
    STRING_SESSION = None # Userbot Session String
    BOTLOG_CHATID = 0 # Logging channel/group configuration.
    BOTLOG = False # Logging channel/group configuration.
    CONSOLE_LOGGER_VERBOSE = False # Console verbose logging
    ALIVE_NAME = None # Default .status name
    CLEAN_WELCOME = True # Clean Welcome
    GREET_STICKER='CAADAgAD0QMAAjq5FQKizo2AiTQCBQI' # Comming soon
    LANG = 'en' #translator language
    HOMIES = [] #Human Of Maximum Intelligence and Empathy, H.O.M.I.E.
    GIRLFRIEND = None
    AUTOMATION_ENABLED = False
    AUTOMATION_SENDERS = [] #IDs
    AUTOMATION_COMMANDS = [] #strings
    AUTOMATION_TRIGGERS = [] #strings
    Q_API_TOKEN = None # Quotly API key http://antiddos.systems
    OPEN_WEATHER_MAP_APPID = None # OWM API key https://openweathermap.org/
    OPEN_WEATHER_MAP_DEFCITY = None # default city to be used for weather

class Development(Config):
    LOGGER = True
  
