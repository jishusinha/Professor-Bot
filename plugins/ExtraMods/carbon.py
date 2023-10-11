from pyrogram import Client, filters
from pyrogram.types import *
from aiohttp import ClientSession
from telegraph import upload_file
from io import BytesIO

ai_client = ClientSession()

async def make_carbon(code, tele=False):
    url = "https://carbonara.solopov.dev/api/cook"
    async with ai_client.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    if tele:
        uf = upload_file(image)
        image.close()
        return f"https://graph.org{uf[0]}"
    return image


@Client.on_message(filters.command("carbon"))
async def carbon_func(b, message):
    if not message.reply_to_message:
        return await message.reply_text("Rᴇᴘʟʏ Tᴏ A Tᴇxᴛ Mᴇssᴀɢᴇ Tᴏ Mᴀᴋᴇ Cᴀʀʙᴏɴ.")
    if not message.reply_to_message.text:
        return await message.reply_text("Rᴇᴘʟʏ Tᴏ A Tᴇxᴛ Mᴇssᴀɢᴇ Tᴏ Mᴀᴋᴇ Cᴀʀʙᴏɴ.")
    user_id = message.from_user.id
    m = await message.reply_text("Pʀᴏᴄᴇssɪɴɢ....")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("Uᴘʟᴏᴀᴅɪɴɢ....")
    await message.reply_photo(
        photo=carbon,
        caption="**Mᴀᴅᴇ Bʏ: @Madflix_Bots**",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Sᴜᴩᴩᴏʀᴛ Uꜱ", url="https://t.me/Madflix_Bots")]]),                   
    )
    await m.delete()
    carbon.close()
