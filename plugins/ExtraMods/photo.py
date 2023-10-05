from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters


@Client.on_message(filters.photo & filters.private)
async def photo_handler(client, message):
    buttons = [[
        InlineKeyboardButton(text="Bʀɪɢᴛʜ", callback_data="bright"),
        InlineKeyboardButton(text="Mɪxᴇᴅ", callback_data="mix"),
        InlineKeyboardButton(text="𝖡 & 𝖶", callback_data="b|w"),
        ],[
        InlineKeyboardButton(text="Cɪʀᴄʟᴇ", callback_data="circle"),
        InlineKeyboardButton(text="Bʟᴜʀ", callback_data="blur"),
        InlineKeyboardButton(text="Bᴏʀᴅᴇʀ", callback_data="border"),
        ],[
        InlineKeyboardButton(text="Sᴛɪᴄᴋᴇʀ", callback_data="stick"),
        InlineKeyboardButton(text="Rᴏᴛᴀᴛᴇ", callback_data="rotate"),
        InlineKeyboardButton(text="Cᴏɴᴛʀᴀsᴛ", callback_data="contrast"),
        ],[
        InlineKeyboardButton(text="Sᴇᴘɪᴀ", callback_data="sepia"),
        InlineKeyboardButton(text="Pᴇɴᴄɪʟ", callback_data="pencil"),
        InlineKeyboardButton(text="Cᴀʀᴛᴏᴏɴ", callback_data="cartoon"),
        ],[
        InlineKeyboardButton(text="Iɴᴠᴇʀᴛ", callback_data="inverted"),
        InlineKeyboardButton(text="Gʟɪᴛᴄʜ", callback_data="glitch"),
        InlineKeyboardButton(text="Rᴇᴍᴏᴠᴇ 𝖡𝖦", callback_data="removebg"),
        ],[
        InlineKeyboardButton(text="Cʟᴏsᴇ", callback_data="close_data"),
    ]]
    try:
        await message.reply(text="Sᴇʟᴇᴄᴛ Yᴏᴜʀ Rᴇǫᴜɪʀᴇᴅ Mᴏᴅᴇ Fʀᴏᴍ Bᴇʟᴏᴡ", quote=True, reply_markup=InlineKeyboardMarkup(buttons))            
    except Exception as e:
        print(e)
        if "USER_IS_BLOCKED" in str(e): return           
        try: await message.reply_text(f"{e} \nSᴏᴍᴇᴛʜɪɴɢ Wᴇɴᴛ Wʀᴏɴɢ !", quote=True)
        except Exception: return
