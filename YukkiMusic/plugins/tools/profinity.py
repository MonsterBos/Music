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
from YukkiMusic.utils.error import capture_err

@app.on_message(filters.text & filters.group, group=11)
@capture_err
async def handle_bad_words(client, message):
    try:
        txt = message.text
        user_id = message.from_user.id
        if not profanity.contains_profanity(txt):
            return

        censored_text = profanity.censor(txt)
        bot_member = await app.get_chat_member(message.chat.id, app.id)
        
        if bot_member is None:
            logging.error("Bot member status could not be retrieved.")
            return
        
        bot = bot_member.privileges
        chat_id = message.chat.id
        admins = []
        async for admin in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
            admins.append(admin.user)

        if user_id in SUDOERS or user_id in [admin.id for admin in admins]:
            return

        if bot is None:
            logging.error("Bot privileges could not be determined.")
            return
        
        for admin in admins:
            if admin.is_bot or admin.is_deleted:
                continue
            censored_text += f"[\u2063](tg://user?id={admin.id})"

        if bot.can_delete_messages and not bot.can_restrict_members:
            await message.delete()
            await message.reply_text(
                f"User {message.from_user.mention} has sent **{censored_text}**. I have deleted the bad word but please give me permission to restrict members in order to automatically mute users who send bad words for 5 minutes."
            )
        elif bot.can_restrict_members and not bot.can_delete_messages:
            mute_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
            await app.restrict_chat_member(chat_id, user_id, ChatPermissions(), until_date=mute_time)
            await message.reply_text(
                f"{message.from_user.mention} used a bad word: **{censored_text}**, so they are muted for 5 minutes but I have no permission to delete messages so give me delete message permission in order to delete bad words automatically."
            )
        elif bot.can_restrict_members and bot.can_delete_messages:
            await message.delete()
            mute_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
            await app.restrict_chat_member(chat_id, user_id, ChatPermissions(), until_date=mute_time)
            SH = await app.send_message(
                message.chat.id,
                f"{message.from_user.mention} used a bad word: **{censored_text}**, so they are muted for 5 minutes.",
            )
            await asyncio.sleep(300)
            await SH.delete()
        elif not bot.can_restrict_members and not bot.can_delete_messages:
            await message.reply_text(
                f"User {message.from_user.mention} has sent **{censored_text}**. The bad word but please give me permission to restrict members in order to automatically mute users who send bad words for 5 minutes and delete message permission to delete bad messages automatically."
            )
    except Exception as e:
        logging.exception(e)
        await app.send_message(LOG_GROUP_ID, f"Error in profanity module: {e}")