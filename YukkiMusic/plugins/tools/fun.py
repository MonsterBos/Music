from pyrogram import Client, filters
from pyrogram.types import Message
from YukkiMusic import app


@app.on_message(filters.command(["dice", "ludo", "dart", "basket", "basketball"]))
async def dice(c, m: Message):
    command = message.text.split()[0]

    value = await c.send_dice(m.chat.id, reply_to_message_id=m.id)
    await value.reply_text("results is {0}".format(value.dice.value))

    value = await c.send_dice(m.chat.id, emoji="🎯", reply_to_message_id=m.id)
    await value.reply_text("results is {0}".format(value.dice.value))

    basket = await c.send_dice(m.chat.id, emoji="🏀", reply_to_message_id=m.id)
    await basket.reply_text("results is {0}".format(basket.dice.value))
