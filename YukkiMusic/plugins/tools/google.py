import logging
from pyrogram import filters
from pyrogram.enums import ChatAction
from googlesearch import search
from YukkiMusic import app
from search_engine_parser.core.engines.bing import Search as BingSearch

import nest_asyncio

bsearch = BingSearch()

nest_asyncio.apply()


@app.on_message(filters.command(["bing"]))
async def google(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text("Example:\n\n`/google lord ram`")
        return

    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        user_input = " ".join(message.command[1:])
    b = await message.reply_text("**Sᴇᴀʀᴄʜɪɴɢ ᴏɴ Gᴏᴏɢʟᴇ....**")
    try:
        search_args = (user_input, 1)
        results = bsearch.search(*search_args)
        await message.reply_text(results)
    except Exception as e:
        await b.edit(e)


@app.on_message(filters.command(["google", "gle"]))
async def google(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text("Example:\n\n`/google lord ram`")
        return

    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        user_input = " ".join(message.command[1:])
    b = await message.reply_text("**Sᴇᴀʀᴄʜɪɴɢ ᴏɴ Gᴏᴏɢʟᴇ....**")
    try:
        a = search(user_input, advanced=True)
        txt = f"Search Query: {user_input}\n\nresults"
        for result in a:
            txt += f"\n\n[❍ {result.title}]({result.url})\n<b>{result.description}</b>"
        await b.edit(
            txt,
            disable_web_page_preview=True,
        )
    except Exception as e:
        await b.edit(e)
        logging.exception(e)


__MODULE__ = "Gᴏᴏɢʟᴇ"
__HELP__ = """/google [ǫᴜᴇʀʏ] - ᴛᴏ sᴇᴀʀᴄʜ ᴏɴ ɢᴏᴏɢʟᴇ ᴀɴᴅ ɢᴇᴛ ʀᴇsᴜʟᴛs"""
