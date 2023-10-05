from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from database.users_chats_db import db
from info import SUPPORT_CHAT
from aiohttp import web
from utils import temp


routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response(text="Mᴀᴅᴇ Bʏ: Mᴀᴅғʟɪx Bᴏᴛᴢ™")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

async def banned_users(_, client, message: Message):
    return (message.from_user is not None or not message.sender_chat) and (message.from_user.id in temp.BANNED_USERS)

async def disabled_chat(_, client, message: Message):
    return message.chat.id in temp.BANNED_CHATS

@Client.on_message(filters.private & filters.incoming & filters.create(banned_users))
async def ban_reply(bot, message):
    ban = await db.get_ban_status(message.from_user.id)
    await message.reply(f"Sᴏʀʀʏ Dᴜᴅᴇ, Yᴏᴜ Aʀᴇ Bᴀɴɴᴇᴅ Tᴏ Usᴇ Mᴇ. \nBᴀɴ Rᴇᴀsᴏɴ: {ban['ban_reason']}")

@Client.on_message(filters.group & filters.incoming & filters.create(disabled_chat))
async def grp_bd(bot, message):
    buttons = [[InlineKeyboardButton('Sᴜᴩᴩᴏʀᴛ', url=f'https://t.me/{SUPPORT_CHAT}')]]
    chat = await db.get_chat(message.chat.id)
    k = await message.reply(text=f"𝙲𝙷𝙰𝚃 𝙽𝙾𝚃 𝙰𝙻𝙻𝙾𝚆𝙴𝙳 🐞\n\nMʏ Aᴅᴍɪɴs Hᴀs Rᴇsᴛʀɪᴄᴛᴇᴅ Mᴇ Fʀᴏᴍ Wᴏʀᴋɪɴɢ Hᴇʀᴇ ! Iғ Yᴏᴜ Wᴀɴᴛ Tᴏ Kɴᴏᴡ Mᴏʀᴇ Aʙᴏᴜᴛ Iᴛ Cᴏɴᴛᴀᴄᴛ Sᴜᴘᴘᴏʀᴛ..\nRᴇᴀꜱᴏɴ : <code>{chat['reason']}</code>.", reply_markup=InlineKeyboardMarkup(buttons))
    try: await k.pin()
    except: pass
    await bot.leave_chat(message.chat.id)
