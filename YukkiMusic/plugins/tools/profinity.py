import logging
import asyncio
import datetime
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import ChatPermissions
from config import LOG_GROUP_ID
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from profanity import profanity


@app.on_message(filters.text & filters.group)
async def handle_bad_words(client, message):
    try:
        txt = message.text
        user_id = message.from_user.id
        if not profanity.contains_profanity(txt):
            return
        censored_text = profanity.censor(txt)
        bot = (await app.get_chat_member(message.chat.id, app.id)).privileges
        chat_id = message.chat.id
        admins = []
        async for admin in app.get_chat_members(
            message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        ):
            admins.append(admin.user)

        if message.from_user.id in SUDOERS or message.from_user.id in [
            admin.id for admin in admins
        ]:
            return
        if bot == None:
            return
        for admin in admins:
            if admin.is_bot or admin.is_deleted:
                continue
            censored_text += f"[\u2063](tg://user?id={admin.id})"

        if bot.can_delete_messages:
            await message.delete()
        else:
            return await message.reply_text(
                f"User {message.from_user.mention} has sended **{censored_text}** bad word give me delete message permission or ban permission to delete and mute user automatically for 5 minute who send bad word"
            )
        if bot.can_restrict_members:
            mute_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
            await app.restrict_chat_member(
                chat_id, user_id, ChatPermissions(), until_date=mute_time
            )
            SH = await app.send_message(
                message.chat.id,
                f"{message.from_user.mention} used a bad word: **{censored_text}**, so they are muted for 5 minutes",
            )
            await asyncio.sleep(300)
            await SH.delete()
        else:
            await app.send_message(
                message.chat.id,
                f"{message.from_user.mention} used a bad word: **{censored_text}**. Please give me ban power to mute users who will send bad words for 5 minutes",
            )

    except Exception as e:
        logging.exception(e)
        await app.send_message(LOG_GROUP_ID, f"Error in profanity module: {e}")
