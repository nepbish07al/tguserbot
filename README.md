# tguserbot

Small userbot for telegram. This project aims to be a simple to use, modular userbot for Telegram users. It is based of [PaperPlane Extended](https://github.com/AvinashReddy3108/PaperplaneExtended), yet completely stripped down and worked on for months. It does not use SQL or any Database entirely. It contains some changes of my own, some commands have been added, a lot removed and some have changed the names to more user friendly names.

Out of the box, most PaperPlane (and PaperPlane Extended) modules *should* work, with a small change in the imports, and maybe the installation of some dependencies.

Updates will be issued incrementally, this is how it will work: example version X.Y.Z. If X increases, major rebase happened, dependencies changed, and possibly entire behaviour, likely it will make past not compatible with this release. If Y increases, features have been added, or big issues have been fixed. If Z increases, common issues have been fixed, simpler update.

## Starting up

Once you have everything ready to start, you can simply run

`python3 -m tg_userbot`

Should ask you for phone number and confirmation code on first boot, but run fine after

## Install guide

Make sure you are running python3.6, I cannot guarantee everything will run fine. Also be sure you are using Telethon 1.10.

Start by installing the python dependencies. In the same directory as requirements.txt run

`python3 -m pip install -r requirements.txt`

This will install all the required dependencies. After this, you need to copy and expand the sample configuration file. Create a new file named `config.py` and make sure in the header you have `from tg_userbot.sample_config import Config`. After that just copy the contents of the Config class in the `sample_config.py` file to your new file, fill in with your data and you should be done. You need your user API key and hash, you can get those in the [Telegram Core API](https://my.telegram.org/) website.

With these done, you should be ready to run your bot, follow the instructions in Starting up section. Good luck.

## Issues

You are welcome to post issues, of course. I will be glad to help and fix your problem. I just ask you to include some steps in how to replicate the problem, so I don't try to fix blindly for nothing.

## Suggestions, contributions and help

Contributions are welcome via pull requests. Try to keep it clean, describe exactly what you did, and if possible comment your changes for easier analysis. Ultimately it is me who decides what makes into the source or not. Suggestions are always welcome, in case you don't know how to code and would like something fixed, adjusted or added. You can do these via the Issues tab of the repo, just start your issue with `[SUGGESTION]`, so I can separate real issues from suggestions and optimize my time.

If the volume of issues or general traffic to the repo justifies it, a Telegram support group will be created and annouced here.

In advance, thank you for your help.

## Special Thanks

Special thanks to my friend [corsicanu](https://github.com/corsicanu) for his help with the configuration file, motivation and hard kick at the start of this project, to my friend [prototype74](https://github.com/prototype74) for his help with some modules and implementation of some functions (such as RTT in webtools) and to my friend [EBY](https://t.me/a52016benutzer) for his motivation and slap ideas.

## Licensing

This project, as with most of my projects, is licensed under GPL-3.0, which means you are free to use it, even for commercial purposes, as long as it stays open source. It is also distributed with no warranty.

The configuration file, however, is distributed under Apache License, version 2.0.
