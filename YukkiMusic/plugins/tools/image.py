import requests
from requests import get
from YukkiMusic import app
from pyrogram import filters
from pyrogram.types import InputMediaPhoto
from bing_image_urls import bing_image_urls


@app.on_message(filters.command(["pinterest"], prefixes=["/", "!", "."]))
async def pinterest(_, message):
    command = message.text.split()[0][1:]
    chat_id = message.chat.id

    try:
        query = message.text.split(None, 1)[1]
    except:
        return await message.reply("**ɢɪᴠᴇ ɪᴍᴀɢᴇ ɴᴀᴍᴇ ғᴏʀ sᴇᴀʀᴄʜ 🔍**")
    if command == "pinterest":
        images = get(f"https://pinterest-api-one.vercel.app/?q={query}").json()
        media_group = []
        count = 0

        msg = await message.reply(f"sᴇᴀʀᴄʜɪɴɢ ɪᴍᴀɢᴇs ғʀᴏᴍ ᴘɪɴᴛᴇʀᴇᴛs...")
        for url in images["images"][:7]:

            media_group.append(InputMediaPhoto(media=url))
            count += 1
            await msg.edit(f"=> ғᴏᴜɴᴅ ɪᴍᴀɢᴇs {count}")

        try:

            await app.send_media_group(
                chat_id=chat_id, media=media_group, reply_to_message_id=message.id
            )
            return await msg.delete()

        except Exception as e:
            return await msg.edit(f"ᴇʀʀᴏʀ : {e}")

    if command == "image":
        images = bing_image_urls(query, limit=15)
        media_group = []
        count = 0

        msg = await message.reply(f"sᴇᴀʀᴄʜɪɴɢ ɪᴍᴀɢᴇs ғʀᴏᴍ ʙɪɴɢ...")
        for url in images:

            media_group.append(InputMediaPhoto(media=url))
            count += 1
            await msg.edit(f"=> ғᴏᴜɴᴅ ɪᴍᴀɢᴇs {count} ғʀᴏᴍ ʙɪɴɢ")

        try:

            await app.send_media_group(
                chat_id=chat_id, media=media_group, reply_to_message_id=message.id
            )
            return await msg.delete()

        except Exception as e:
            return await msg.edit(f"ᴇʀʀᴏʀ : {e}")


__MODULE__ = "Iᴍᴀɢᴇ"
__HELP__ = """/pinterest [ǫᴜᴇʀʏ] - ᴛᴏ ɢᴇᴛ ᴛᴏᴘ 7 ɪᴍᴀɢᴇs ғʀᴏᴍ ᴘɪɴᴛᴇʀᴇsᴛ
/cat - ɢᴇᴛ ʀᴀɴᴅᴏᴍ ᴄᴀᴛ ɪᴍᴀɢᴇs
/dog - ɢᴇᴛ ʀᴀɴᴅᴏᴍ ᴅᴏɢ ɪᴍᴀɢᴇs
"""
