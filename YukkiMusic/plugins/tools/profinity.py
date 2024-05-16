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
        chat_id = message.chat.id
        txt = message.text
        user_id = message.from_user.id
        admins = []
        async for admin in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
            admins.append(admin.user)

        if message.from_user.id in SUDOERS or message.from_user.id in [
            admin.id for admin in admins
        ]:
            return

        bot = await app.get_chat_member(message.chat.id, app.id).privileges
        if bot == None:
            return

        if profanity.contains_profanity(txt):
            await message.delete()
            censored_text = profanity.censor(txt)
            for admin in admins:
                if admin.is_bot or admin.is_deleted:
                    continue
                censored_text += f"[\u2063](tg://user?id={admin.id})"

            if bot.can_restrict_members:
                mute_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
                await app.restrict_chat_member(
                    chat_id, user_id, ChatPermissions(), until_date=mute_time
                )
                SH = await app.send_message(
                    message.chat.id,
                    f"{message.from_user.mention} used a bad word: **{censored_text}**, so they are muted for 5 minutes {mentioned_admins}",
                )
            else:
                SH = await app.send_message(
                    message.chat.id,
                    f"{message.from_user.mention} used a bad word: **{censored_text}**. Please give me ban power to mute users who send bad words for 5 minutes {mentioned_admins}",
                )

            await asyncio.sleep(300)
            await SH.delete()
        else:
            return

    except Exception as e:
        logging.exception(e)
        await app.send_message(LOG_GROUP_ID, f"Error in profanity module: {e}")
