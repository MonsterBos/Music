from pyrogram import Client, filters
from profanity_check import predict, predict_prob
from YukkiMusic import app

@app.on_message(filters.private)
async def check_for_profanity(client, message):
    text = message.text.lower() if message.text else ""
    if predict_prob([text])[0] > 0.5:
        await message.reply("Please refrain from using profanity.")
    else:
        pass
