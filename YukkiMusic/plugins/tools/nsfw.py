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
    ~filters.service & ~filters.private & ~filters.channel & filters.photo, group=6
)
@capture_err
async def nsfw(_, message: Message):
    admins = adminlist.get(message.chat.id)
    if message.from_user.id in admins or message.from_user.id in SUDOERS:
        return

    photo = await app.download_media(message.photo.file_id)
    uploaded_file = upload_file(photo)[0]
    url = "https://telegra.ph" + uploaded_file
    try:
        nsfw = check_nsfw(url)
        if nsfw == True:
            await message.reply_text("NSFW content detected")
        else:
            await message.reply_text("Safe file, no NSFW content detected")
        remove(photo)
    except Exception as e:
        remove(photo)
        logging.exception(e)