import logging
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from profanity import profanity
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import ChatAdminRequired
from config import LOG_GROUP_ID


@app.on_message(filters.text & filters.group)
async def handle_bad_words(client, message):
    try:
        chat_id = message.chat.id
        txt = message.text
        user_id = message.from_user.id
        admins = []
        async for i in app.get_chat_members(
            message.chat.id,
            filter=ChatMembersFilter.ADMINISTRATORS or ChatMembersFilter.OWNER,
        ):
            admins.append(i.user.id)

        if message.from_user.id in SUDOERS or message.from_user.id in admins:
            return
        bot = (await app.get_chat_member(message.chat.id, app.id)).privileges
        if profanity.contains_profanity(txt) == True:
            await message.delete()
            if bot == None:
                return
            B = profanity.censor(txt)
            for admin in admins:
                if admin.user.is_bot or admin.user.is_deleted:
                    continue
                B += f"[\u2063](tg://user?id={admin.user.id})"
            if bot.can_restrict_members:
                mute_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
                await app.restrict_chat_member(
                    chat_id, user_id, ChatPermissions(), until_date=mute_time
                )
                Sh = await app.send_message(
                    message.chat.id,
                    f"{message.from_user.mention} used a badword :- **{B}** so he is  muted for 5 minutes ",
                )
            else:
                Sh = await app.send_message(
                    message.chat.id,
                    f"{message.from_user.mention} used a badword :- **{B}** Give me ban power so i mute who send bad word for 5 minutes",
                )

            await asyncio.sleep(300)
            await Sh.delete()
        else:
            return

    except Exception as e:
        logging.exception(e)
        await app.send_message(LOG_GROUP_ID, f" in profanity module {e} ")
