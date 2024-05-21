from pyrogram import Client, filters
from pyrogram.types import Message
from YukkiMusic import app


@app.on_message(filters.command(["dice", "ludo"]))
async def dice(c, m: Message):
    dicen = await c.send_dice(m.chat.id, reply_to_message_id=m.id)
    await dicen.reply_text("results is {0}".format(dicen.dice.value))


@app.on_message(filters.command(["dart"]))
async def dice(c, m: Message):
    dart = await c.send_dice(m.chat.id, emoji="🎯", reply_to_message_id=m.id)
    await dart.reply_text("results is {0}".format(dart.dice.value))


@app.on_message(filters.command(["basket", "basketball"]))
async def dice(c, m: Message):
    basket = await c.send_dice(m.chat.id, emoji="🏀", reply_to_message_id=m.id)
    await basket.reply_text("results is {0}".format(basket.dice.value))
