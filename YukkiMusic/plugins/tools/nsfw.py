import logging 
from os import remove
from lexica import Client as lexi
from telegraph import upload_file
from pyrogram import filters
from pyrogram.types import Message
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils.error import capture_err
from config import adminlist

def check_nsfw(image_url: str) -> dict:
    client = lexi()
    response = client.AntiNsfw(image_url)
    if response['content']['sfw'] == True:
        return False
    else:
        return True       

@app.on_message(
    ~filters.service
    & ~filters.private
    & ~filters.channel
    & filters.photo,
    group=6
)

@capture_err
async def nsfw(_, message: Message):
    admins = adminlist.get(message.chat.id)
    if message.from_user.id in admins or message.from_user.id in SUDOERS:
        return 

    photo = await app.download_media(message.photo.file_id)
    a = upload_file(media)[0]
    url = "https://telegra.ph" + a
    try:
	nsfw = check_nsfw(url)
        if nsfw == True:
            await message.reply_text("Nsfw detected")
            remove(photo)
        elif nsfw == False:
	    await message.reply_text("safe file no nsfw detected")
	    remove(photo)
    except Exception as e:
        remove(photo)
        logging.execption(e)

	
