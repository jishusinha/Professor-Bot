from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.connections_mdb import add_connection, all_connections, if_active, delete_connection
from info import ADMINS
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


@Client.on_message((filters.private | filters.group) & filters.command('connect'))
async def addconnection(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"Yᴏᴜ Aʀᴇ Aɴᴏɴʏᴍᴏᴜs Aᴅᴍɪɴ. Usᴇ /connect {message.chat.id} Iɴ PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        try:
            cmd, group_id = message.text.split(" ", 1)
        except:
            await message.reply_text(
                "<b>Eɴᴛᴇʀ Iɴ Cᴏʀʀᴇᴄᴛ Fᴏʀᴍᴀᴛ!</b>\n\n"
                "<code>/connect groupid</code>\n\n"
                "<i>Get your Group id by adding this bot to your group and use  <code>/id</code></i>",
                quote=True
            )
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        group_id = message.chat.id

    try:
        st = await client.get_chat_member(group_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and userid not in ADMINS
        ):
            return await message.reply_text("Yᴏᴜ Sʜᴏᴜʟᴅ Bᴇ Aɴ Aᴅᴍɪɴ Iɴ Gɪᴠᴇɴ Gʀᴏᴜᴘ!", quote=True)
    except Exception as e:
        logger.exception(e)
        return await message.reply_text("Iɴᴠᴀʟɪᴅ Gʀᴏᴜᴘ ID!\n\nIғ Cᴏʀʀᴇᴄᴛ, Mᴀᴋᴇ Sᴜʀᴇ I'ᴍ Pʀᴇsᴇɴᴛ Iɴ Yᴏᴜʀ Gʀᴏᴜᴘ!!", quote=True,)
    try:
        st = await client.get_chat_member(group_id, "me")
        if st.status == enums.ChatMemberStatus.ADMINISTRATOR:
            ttl = await client.get_chat(group_id)
            title = ttl.title

            addcon = await add_connection(str(group_id), str(userid))
            if addcon:
                await message.reply_text(
                    f"Sᴜᴄᴄᴇssғᴜʟʟʏ Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ **{title}**\nNᴏᴡ Mᴀɴᴀɢᴇ Yᴏᴜʀ Gʀᴏᴜᴘ Fʀᴏᴍ Mʏ PM !",
                    quote=True,
                    parse_mode=enums.ParseMode.MARKDOWN
                )
                if chat_type in ["group", "supergroup"]:
                    await client.send_message(
                        userid,
                        f"Connected to **{title}** !",
                        parse_mode=enums.ParseMode.MARKDOWN
                    )
            else:
                await message.reply_text("Yᴏᴜ'ʀᴇ Aʟʀᴇᴀᴅʏ Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ Tʜɪs Cʜᴀᴛ !", quote=True)
        else:
            await message.reply_text("Aᴅᴅ Mᴇ As Aɴ Aᴅᴍɪɴ Iɴ Gʀᴏᴜᴘ", quote=True)
    except Exception as e:
        logger.exception(e)
        return await message.reply_text('Sᴏᴍᴇ Eʀʀᴏʀ Oᴄᴄᴜʀʀᴇᴅ! Tʀʏ Aɢᴀɪɴ Lᴀᴛᴇʀ.', quote=True)
     

@Client.on_message((filters.private | filters.group) & filters.command('disconnect'))
async def deleteconnection(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"Yᴏᴜ Aʀᴇ Aɴᴏɴʏᴍᴏᴜs Aᴅᴍɪɴ. Usᴇ /connect {message.chat.id} Iɴ PM")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        await message.reply_text("Usᴇ /connections Tᴏ Vɪᴇᴡ Oʀ Dɪsᴄᴏɴɴᴇᴄᴛ Fʀᴏᴍ Gʀᴏᴜᴘs !", quote=True)
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        group_id = message.chat.id

        st = await client.get_chat_member(group_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            return

        delcon = await delete_connection(str(userid), str(group_id))
        if delcon:
            await message.reply_text("Sᴜᴄᴄᴇssғᴜʟʟʏ Dɪsᴄᴏɴɴᴇᴄᴛᴇᴅ Fʀᴏᴍ Tʜɪs Cʜᴀᴛ", quote=True)
        else:
            await message.reply_text("Tʜɪs Cʜᴀᴛ Isɴ'ᴛ Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ Mᴇ !\nDᴏ /connect Tᴏ Cᴏɴɴᴇᴄᴛ.", quote=True)


@Client.on_message(filters.private & filters.command(["connections"]))
async def connections(client, message):
    userid = message.from_user.id
    groupids = await all_connections(str(userid))
    if groupids is None:
        return await message.reply_text("Tʜᴇʀᴇ Aʀᴇ Nᴏ Aᴄᴛɪᴠᴇ Cᴏɴɴᴇᴄᴛɪᴏɴs!! Cᴏɴɴᴇᴄᴛ Tᴏ Sᴏᴍᴇ Gʀᴏᴜᴘs Fɪʀsᴛ.", quote=True)
    buttons = []
    for groupid in groupids:
        try:
            ttl = await client.get_chat(int(groupid))
            title = ttl.title
            active = await if_active(str(userid), str(groupid))
            act = " - ACTIVE" if active else ""
            buttons.append([InlineKeyboardButton(f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}")])
        except:
            pass
    if buttons:
        await message.reply_text("Your connected group details ;\n\n", reply_markup=InlineKeyboardMarkup(buttons), quote=True)
    else:
        await message.reply_text("Tʜᴇʀᴇ Aʀᴇ Nᴏ Aᴄᴛɪᴠᴇ Cᴏɴɴᴇᴄᴛɪᴏɴs!! Cᴏɴɴᴇᴄᴛ Tᴏ Sᴏᴍᴇ Gʀᴏᴜᴘs Fɪʀsᴛ.", quote=True)
