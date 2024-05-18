# Copyright (C) 2024-present by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
#

import sys
import config
import asyncio
import importlib
from sys import argv

from pyrogram import idle, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import BANNED_USERS

from YukkiMusic import LOGGER, app, userbot
from YukkiMusic import telethn
from YukkiMusic.core.call import Yukki
from YukkiMusic.plugins import ALL_MODULES
from YukkiMusic.utils.database import get_banned_users, get_gbanned
from YukkiMusic.utils.inlinefunction import is_module_loaded, paginate_modules

# from YukkiMusic.plugins.tools.clone import restart_bots

loop = asyncio.get_event_loop_policy().get_event_loop()
HELPABLE = {}


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("YukkiMusic").error(
            "No Assistant Clients Vars Defined!.. Exiting Process."
        )
        return
    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("YukkiMusic").warning(
            "No Spotify Vars defined. Your bot won't be able to play spotify queries."
        )
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        imported_module = importlib.import_module("YukkiMusic.plugins" + all_module)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    LOGGER("Yukkimusic.plugins").info("Successfully Imported Modules ")
    # await restart_bots()
    await userbot.start()
    await Yukki.start()
    await Yukki.decorators()
    LOGGER("YukkiMusic").info("Yukki Music Bot Started Successfully")
    await idle()
    if len(argv) not in (1, 3, 4):
        await telethn.disconnect()
    else:
        await telethn.run_until_disconnected()


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        """ʜᴇʟʟᴏ {first_name},

ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.

ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs sᴛᴀʀᴛsᴡɪᴛʜ :-  /
""".format(
            first_name=name
        ),
        keyboard,
    )


@app.on_callback_query(filters.regex("shikharbro"))
async def shikhar(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await CallbackQuery.message.edit(text, reply_markup=keyboard)


if __name__ == "__main__":
    telethn.start(bot_token=config.BOT_TOKEN)
    loop.run_until_complete(init())
    LOGGER("YukkiMusic").info("Stopping Yukki Music Bot! GoodBye")
