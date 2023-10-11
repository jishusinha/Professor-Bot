import os
from pyrogram import Client, filters
from urllib.parse import quote
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command(["share_text", "share", "sharetext",]))
async def share_text(client, message):
    reply = message.reply_to_message
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    input_split = message.text.split(None, 1)
    if len(input_split) == 2:
        input_text = input_split[1]
    elif reply and (reply.text or reply.caption):
        input_text = reply.text or reply.caption
    else:
        await message.reply_text(
            text=f"**Nᴏᴛɪᴄᴇ:**\n\n1. Rᴇᴘʟʏ Aɴʏ Mᴇssᴀɢᴇs.\n2. Nᴏ Mᴇᴅɪᴀ Sᴜᴘᴘᴏʀᴛ\n\n**Aɴʏ Qᴜᴇsᴛɪᴏɴ Jᴏɪɴ Sᴜᴘᴘᴏʀᴛ Cʜᴀᴛ**",                
            reply_to_message_id=reply_id,               
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ Cʜᴀᴛ", url=f"https://t.me/MadflixBots_Support")]])
            )                                                   
        return
    await message.reply_text(
        text=f"**Hᴇʀᴇ Is Yᴏᴜʀ Sʜᴀʀɪɴɢ Tᴇxᴛ 👇**\n\nhttps://t.me/share/url?url=" + quote(input_text),
        reply_to_message_id=reply_id,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("♂️ Sʜᴀʀᴇ", url=f"https://t.me/share/url?url={quote(input_text)}")]])       
    )
