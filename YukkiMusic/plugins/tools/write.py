import os
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
import requests
from io import BytesIO


def text_set(text):
    lines = []
    if len(text) <= 55:
        lines.append(text)
    else:
        all_lines = text.split("\n")
        for line in all_lines:
            if len(line) <= 55:
                lines.append(line)
            else:
                k = len(line) // 55
                lines.extend(line[((z - 1) * 55) : (z * 55)] for z in range(1, k + 2))
    return lines[:25]


@app.on_message(filters.command(["write"]))
async def handwrite(client, message):
    if message.reply_to_message and message.reply_to_message.text:
        txt = message.reply_to_message.text
    elif len(message.command) > 1:
        txt = message.text.split(None, 1)[1]
    else:
        return await message.reply(
            "Please reply to message or write after command to use write CMD."
        )
    nan = await message.reply_text("Processing...")
    try:
        # Download the image
        img_url = "https://graph.org/file/00552e0917279fc954711.jpg"
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))

        # Download the Poetsen One Regular font from GitHub
        font_url = "https://github.com/google/fonts/raw/main/ofl/poetsenone/PoetsenOne-Regular.ttf"
        font_response = requests.get(font_url)
        font = ImageFont.truetype(BytesIO(font_response.content), 20)

        draw = ImageDraw.Draw(img)
        x, y = 150, 140
        lines = text_set(txt)
        line_height = font.getbbox("hg")[3]
        for line in lines:
            draw.text((x, y), line, fill=(1, 22, 55), font=font)
            y = y + line_height - 5

        file = f"write_{message.from_user.id}.jpg"
        img.save(file)
        if os.path.exists(file):
            await message.reply_photo(
                photo=file, caption=f"<b>Written By :</b> {client.me.mention}"
            )
            os.remove(file)
            await nan.delete()
    except Exception as e:
        os.remove(file)
        return await message.reply(str(e))


__MODULE__ = "ᴡʀɪᴛᴇ"
__HELP__ = """
/write [ʏᴏᴜʀ ᴛᴇxᴛ] - Tᴏ ᴡʀɪᴛᴇ ɪɴ ᴀ ᴘᴀɢᴇ ᴏғ ɴᴏᴛᴇʙᴏᴏᴋ"""
