import logging, re, asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from info import CHANNELS, LOG_CHANNEL, ADMINS
from database.ia_filterdb import save_file
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import temp

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lock = asyncio.Lock()


@Client.on_message(filters.chat(CHANNELS) & (filters.document | filters.video | filters.audio))         
async def media(bot, message):
    for file_type in ("document", "video", "audio"):
        media = getattr(message, file_type, None)
        if media is not None: break
    else: return
    media.file_type = file_type
    media.caption = message.caption
    await save_file(media)



@Client.on_callback_query(filters.regex(r'^index'))
async def index_files(bot, query):
    if query.data.startswith('index_cancel'):
        temp.CANCEL = True
        return await query.answer("Cᴀɴᴄᴇʟʟɪɴɢ Iɴᴅᴇxɪɴɢ", show_alert=True)
        
    perfx, chat, lst_msg_id = query.data.split("#")
    if lock.locked():
        return await query.answer('Wᴀɪᴛ Uɴᴛɪʟ Pʀᴇᴠɪᴏᴜs Pʀᴏᴄᴇss Cᴏᴍᴘʟᴇᴛᴇ', show_alert=True)
    msg = query.message
    button = InlineKeyboardMarkup([[
        InlineKeyboardButton('🚫 Cᴀɴᴄᴇʟ', "index_cancel")
    ]])
    await msg.edit("Iɴᴅᴇxɪɴɢ Is Sᴛᴀʀᴛᴇᴅ ✨", reply_markup=button)                        
    try: chat = int(chat)
    except: chat = chat
    await index_files_to_db(int(lst_msg_id), chat, msg, bot)


@Client.on_message((filters.forwarded | (filters.regex("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")) & filters.text ) & filters.private & filters.incoming & filters.user(ADMINS))
async def send_for_index(bot, message):
    if message.text:
        regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(message.text)
        if not match: return await message.reply('Invalid link')
        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric(): chat_id  = int(("-100" + chat_id))
    elif message.forward_from_chat.type == enums.ChatType.CHANNEL:
        last_msg_id = message.forward_from_message_id
        chat_id = message.forward_from_chat.username or message.forward_from_chat.id
    else: return
    try: await bot.get_chat(chat_id)
    except ChannelInvalid: return await message.reply('Tʜɪs Mᴀʏ Bᴇ A Pʀɪᴠᴀᴛᴇ Cʜᴀɴɴᴇʟ / Gʀᴏᴜᴘ. Mᴀᴋᴇ Mᴇ Aɴ Aᴅᴍɪɴ Oᴠᴇʀ Tʜᴇʀᴇ Tᴏ Iɴᴅᴇx Tʜᴇ Fɪʟᴇs.')
    except (UsernameInvalid, UsernameNotModified): return await message.reply('Iɴᴠᴀʟɪᴅ Lɪɴᴋ Sᴘᴇᴄɪғɪᴇᴅ.')
    except Exception as e: return await message.reply(f'Errors - {e}')
    try: k = await bot.get_messages(chat_id, last_msg_id)
    except: return await message.reply('Mᴀᴋᴇ Sᴜʀᴇ Tʜᴀᴛ Iᴀᴍ Aɴ Aᴅᴍɪɴ Iɴ Tʜᴇ Cʜᴀɴɴᴇʟ, Iғ Cʜᴀɴɴᴇʟ Is Pʀɪᴠᴀᴛᴇ')
    if k.empty: return await message.reply('Tʜɪs Mᴀʏ Bᴇ Gʀᴏᴜᴘ Aɴᴅ I Aᴍ Nᴏᴛ A Aᴅᴍɪɴ Oғ Tʜᴇ Gʀᴏᴜᴘ.')
    buttons = InlineKeyboardMarkup([[
        InlineKeyboardButton('🩵 Yᴇꜱ', callback_data=f'index#{chat_id}#{last_msg_id}')
        ],[
        InlineKeyboardButton('🚫 Cʟᴏꜱᴇ', callback_data='close_data')
    ]])               
    await message.reply(f'Dᴏ Yᴏᴜ Wᴀɴᴛ Tᴏ Iɴᴅᴇx Tʜɪs Cʜᴀɴɴᴇʟ/ Gʀᴏᴜᴘ ?\n\nCʜᴀᴛ ID/ Usᴇʀɴᴀᴍᴇ: <code>{chat_id}</code>\nLᴀsᴛ Mᴇssᴀɢᴇ ID: <code>{last_msg_id}</code>', reply_markup=buttons)
    

@Client.on_message(filters.command('setskip') & filters.user(ADMINS))
async def set_skip_number(bot, message):
    if len(message.command) == 2:
        try: skip = int(message.text.split(" ", 1)[1])
        except: return await message.reply("Sᴋɪᴘ Nᴜᴍʙᴇʀ Sʜᴏᴜʟᴅ Bᴇ Aɴ Iɴᴛᴇɢᴇʀ.")
        await message.reply(f"Sᴜᴄᴄᴇssғᴜʟʟʏ Sᴇᴛ Sᴋɪᴘ Nᴜᴍʙᴇʀ As {skip}")
        temp.CURRENT = int(skip)
    else:
        await message.reply("Gɪᴠᴇ Mᴇ A Sᴋɪᴘ Nᴜᴍʙᴇʀ")


async def index_files_to_db(lst_msg_id, chat, msg, bot):
    total_files = 0
    duplicate = 0
    errors = 0
    deleted = 0
    no_media = 0
    unsupported = 0
    async with lock:
        try:
            current = temp.CURRENT
            temp.CANCEL = False
            async for message in bot.iter_messages(chat, lst_msg_id, temp.CURRENT):
                if temp.CANCEL:
                    await msg.edit(f"Sᴜᴄᴄᴇssғᴜʟʟʏ Cᴀɴᴄᴇʟʟᴇᴅ!!\n\nSᴀᴠᴇᴅ <code>{total_files}</code> Fɪʟᴇs Tᴏ Dᴀᴛᴀʙᴀsᴇ!\nDᴜᴘʟɪᴄᴀᴛᴇ Fɪʟᴇs Sᴋɪᴘᴘᴇᴅ: <code>{duplicate}</code>\nDᴇʟᴇᴛᴇᴅ Mᴇssᴀɢᴇs Sᴋɪᴘᴘᴇᴅ: <code>{deleted}</code>\nNᴏɴ-Mᴇᴅɪᴀ Mᴇssᴀɢᴇs Sᴋɪᴘᴘᴇᴅ: <code>{no_media + unsupported}</code>(Unsupported Media - `{unsupported}` )\nEʀʀᴏʀs Oᴄᴄᴜʀʀᴇᴅ: <code>{errors}</code>")
                    break
                current += 1
                if current % 100 == 0:
                    can = [[InlineKeyboardButton('Cancel', callback_data='index_cancel')]]
                    reply = InlineKeyboardMarkup(can)
                    try:
                        await msg.edit_text(text=f"Tᴏᴛᴀʟ Mᴇssᴀɢᴇs Fᴇᴛᴄʜᴇᴅ: <code>{current}</code>\nTᴏᴛᴀʟ Mᴇssᴀɢᴇs Sᴀᴠᴇᴅ: <code>{total_files}</code>\nDᴜᴘʟɪᴄᴀᴛᴇ Fɪʟᴇs Sᴋɪᴘᴘᴇᴅ: <code>{duplicate}</code>\nDᴇʟᴇᴛᴇᴅ Mᴇssᴀɢᴇs Sᴋɪᴘᴘᴇᴅ: <code>{deleted}</code>\nNᴏɴ-Mᴇᴅɪᴀ Mᴇssᴀɢᴇs Sᴋɪᴘᴘᴇᴅ: <code>{no_media + unsupported}</code>(Unsupported Media - `{unsupported}` )\nEʀʀᴏʀs Oᴄᴄᴜʀʀᴇᴅ: <code>{errors}</code>", reply_markup=reply)       
                    except FloodWait as t:
                        await asyncio.sleep(t.value)
                        await msg.edit_text(text=f"Tᴏᴛᴀʟ Mᴇssᴀɢᴇs Fᴇᴛᴄʜᴇᴅ: <code>{current}</code>\nTᴏᴛᴀʟ Mᴇssᴀɢᴇs Sᴀᴠᴇᴅ: <code>{total_files}</code>\nDᴜᴘʟɪᴄᴀᴛᴇ Fɪʟᴇs Sᴋɪᴘᴘᴇᴅ: <code>{duplicate}</code>\nDᴇʟᴇᴛᴇᴅ Mᴇssᴀɢᴇs Sᴋɪᴘᴘᴇᴅ: <code>{deleted}</code>\nNᴏɴ-Mᴇᴅɪᴀ Mᴇssᴀɢᴇs Sᴋɪᴘᴘᴇᴅ: <code>{no_media + unsupported}</code>(Unsupported Media - `{unsupported}` )\nEʀʀᴏʀs Oᴄᴄᴜʀʀᴇᴅ: <code>{errors}</code>", reply_markup=reply)                          
                if message.empty:
                    deleted += 1
                    continue
                elif not message.media:
                    no_media += 1
                    continue
                elif message.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.AUDIO, enums.MessageMediaType.DOCUMENT]:
                    unsupported += 1
                    continue
                media = getattr(message, message.media.value, None)
                if not media:
                    unsupported += 1
                    continue
                media.file_type = message.media.value
                media.caption = message.caption
                aynav, vnay = await save_file(media)
                if aynav:
                    total_files += 1
                elif vnay == 0:
                    duplicate += 1
                elif vnay == 2:
                    errors += 1       
        except Exception as e:
            logger.exception(e)
            await msg.edit(f'Error: {e}')
        else:
            await msg.edit(f'Sᴜᴄᴄᴇsғᴜʟʟʏ Sᴀᴠᴇᴅ <code>{total_files}</code> Tᴏ Dᴀᴛᴀʙᴀsᴇ!\nDᴜᴘʟɪᴄᴀᴛᴇ Fɪʟᴇs Sᴋɪᴘᴘᴇᴅ: <code>{duplicate}</code>\nDᴇʟᴇᴛᴇᴅ Mᴇssᴀɢᴇs Sᴋɪᴘᴘᴇᴅ: <code>{deleted}</code>\nNᴏɴ-Mᴇᴅɪᴀ Mᴇssᴀɢᴇs Sᴋɪᴘᴘᴇᴅ: <code>{no_media + unsupported}</code>(Unsupported Media - `{unsupported}` )\nEʀʀᴏʀs Oᴄᴄᴜʀʀᴇᴅ: <code>{errors}</code>')





