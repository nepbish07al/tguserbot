"""
This module updates the userbot based on Upstream revision
"""

import asyncio
import sys
from os import remove, environ, execle

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from tg_userbot import CMD_HELP, UPSTREAM_REPO_URL
from tg_userbot.events import register


async def gen_chlog(repo, diff):
    ch_log = ''
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += f'•[{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n'
    return ch_log


async def is_off_br(br):
    off_br = ['master', 'staging', 'redis']
    if br in off_br:
        return 1
    return


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            ' '.join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


@register(outgoing=True, pattern="^.update(?: |$)(.*)")
async def upstream(ups):
    if not ups.text[0].isalpha() and ups.text[0] in ("."):
        await ups.edit("`Checking for updates, please wait....`")
        conf = ups.pattern_match.group(1)
        off_repo = UPSTREAM_REPO_URL

        try:
            txt = "`Oops.. Updater cannot continue due to "
            txt += "some problems occured`\n\n**LOGTRACE:**\n"
            repo = Repo()
        except NoSuchPathError as error:
            await ups.edit(f'{txt}\n`directory {error} is not found`')
            return
        except InvalidGitRepositoryError as error:
            await ups.edit(f'{txt}\n`directory {error} does \
                            not seems to be a git repository`')
            return
        except GitCommandError as error:
            await ups.edit(f'{txt}\n`Early failure! {error}`')
            return

        ac_br = repo.active_branch.name
        if not await is_off_br(ac_br):
            await ups.edit(
                f'**[UPDATER]:**` Looks like you are using your own custom branch ({ac_br}). '
                'in that case, Updater is unable to identify '
                'which branch is to be merged. '
                'please checkout to any official branch`')
            return

        try:
            repo.create_remote('upstream', off_repo)
        except BaseException:
            pass

        ups_rem = repo.remote('upstream')
        ups_rem.fetch(ac_br)
        changelog = await gen_chlog(repo, f'HEAD..upstream/{ac_br}')

        if not changelog:
            await ups.edit(
                f'\n`Your BOT is`  **up-to-date**  `with`  **{ac_br}**\n')
            return

        if conf != "now":
            changelog_str = f'**New UPDATE available for [{ac_br}]:\n\nCHANGELOG:**\n`{changelog}`'
            if len(changelog_str) > 4096:
                await ups.edit("`Changelog is too big, view the file to see it.`")
                file = open("output.txt", "w+")
                file.write(changelog_str)
                file.close()
                await ups.client.send_file(
                    ups.chat_id,
                    "output.txt",
                    reply_to=ups.id,
                )
                remove("output.txt")
            else:
                await ups.edit(changelog_str)
            await ups.respond('`do \".update now\" to update`')
            return

        await ups.edit('`New update found, updating...`')
        ups_rem.fetch(ac_br)
        repo.git.reset('--hard', 'FETCH_HEAD')
        # reqs_upgrade = await update_requirements()
        await ups.edit('`Successfully Updated!\n'
                       'Bot is restarting... Wait for a second!`')
        # Spin a new instance of bot
        args = [sys.executable, "-m", "tg_userbot"]
        execle(sys.executable, *args, environ)
        return

@register(outgoing=True, pattern="^.reboot(?: |$)(.*)")
async def upstream(ups):
    await ups.edit('`Rebooting...`')
    args = [sys.executable, "-m", "tg_userbot"]
    execle(sys.executable, *args, environ)
    await ups.edit("`Sucessfully rebooted!`")
    return

CMD_HELP.update(
    {"updater": "`.update`: Check if the main repository has any updates and show changelog if so.\
        \n\n`.update now`: Update tguserbot if there are any updates available."})
