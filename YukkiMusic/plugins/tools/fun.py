from pyrogram import filters
from pyrogram.types import Message
from YukkiMusic import app


@app.on_message(filters.command(["dice", "ludo", "dart", "basket", "basketball","football","slot","bowling","jackpot"]))
async def dice(c, m: Message):
    command = message.text.split()[0]
    if command == "/dice" or command == "/ludo":
    	
        value = await c.send_dice(m.chat.id, reply_to_message_id=m.id)
        await value.reply_text("ʏᴏᴜʀ sᴄᴏʀᴇ ɪs {0}".format(value.dice.value))
        
    if command == "/dart":
    	
        value = await c.send_dice(m.chat.id, emoji="🎯", reply_to_message_id=m.id)
        await value.reply_text("ʏᴏᴜʀ sᴄᴏʀᴇ ɪs {0}".format(value.dice.value))
        
    if command == "/basket" or command == "/basketball":
    basket = await c.send_dice(m.chat.id, emoji="🏀", reply_to_message_id=m.id)
    await basket.reply_text("ʏᴏᴜʀ sᴄᴏʀᴇ ɪs {0}".format(basket.dice.value))
    
    if command == "/football":
        value = await c.send_dice(m.chat.id, emoji="⚽", reply_to_message_id=m.id)
        await value.reply_text("ʏᴏᴜʀ sᴄᴏʀᴇ ɪs {0}".format(value.dice.value))
        
     if command == "/slot" or command == "/jackpot":
        value = await c.send_dice(m.chat.id, emoji="🎰", reply_to_message_id=m.id)
        await value.reply_text("ʏᴏᴜʀ sᴄᴏʀᴇ ɪs {0}".format(value.dice.value))
     if command == "/bowling":
        value = await c.send_dice(m.chat.id, emoji="🎳", reply_to_message_id=m.id)
        await value.reply_text("ʏᴏᴜʀ sᴄᴏʀᴇ ɪs {0}".format(value.dice.value))
     

__MODULE__ = "Fᴜɴ"
__HELP__ = """
/dice - sᴇɴᴅ ᴛʜᴇ 🎲 ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ sᴄᴏʀᴇ
/dart - sᴇɴᴅ ᴛʜᴇ 🎯 ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ sᴄᴏʀᴇ
/basketball - sᴇɴᴅ ᴛʜᴇ 🏀 ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ sᴄᴏʀᴇ
/football - sᴇɴᴅ ᴛʜᴇ ⚽ ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ sᴄᴏʀᴇ
/jackpot - sᴇɴᴅ ᴛʜᴇ 🎰 ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ sᴄᴏʀᴇ
/bowling - sᴇɴᴅ ᴛʜᴇ  🎳 ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ sᴄᴏʀᴇ
"""
