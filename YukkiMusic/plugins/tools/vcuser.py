from pytgcalls.exceptions import GroupCallNotFound
from pyrogram import filters
from YukkiMusic.core.call import Yukki
from YukkiMusic import app
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid


@app.on_message(filters.command("vcuser"))
async def get_vc_users(client, message):
    try:
        A = await message.replt_text("🔍")
        AB = await Yukki.get_participant(message.chat.id)
    except GroupCallNotFound:
        return await message.reply_text("Assisitant iss not in vc")
    users_info = ""
    for participant in AB:
        user_id = participant.user_id
        try:
            user = await app.get_users(user_id)
            users_info += f"[{user.first_name}](tg://user?id={user_id})\n"
        except PeerIdInvalid:
            users_info += f"[ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ](tg://user?id={user_id})\n"

    await A.edit(users_info)
