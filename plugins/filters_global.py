import io
from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.filters_mdb import add_filter, get_filters, delete_filter, count_filters
from database.gfilters_mdb import add_gfilter, get_gfilters, delete_gfilter, count_gfilters, del_allg
from database.connections_mdb import active_connection
from utils import get_file_id, parser, split_quotes
from info import ADMINS



@Client.on_message(filters.command(['filter', 'add']) & filters.incoming)
async def addfilter(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"Yᴏᴜ Aʀᴇ Aɴᴏɴʏᴍᴏᴜs Aᴅᴍɪɴ. Usᴇ /connect {message.chat.id} Iɴ PM")
    chat_type = message.chat.type
    args = message.text.html.split(None, 1)

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Mᴀᴋᴇ Sᴜʀᴇ I'ᴍ Pʀᴇsᴇɴᴛ Iɴ Yᴏᴜʀ Gʀᴏᴜᴘ !!", quote=True)
                return
        else:
            await message.reply_text("I'ᴍ Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ Aɴʏ Gʀᴏᴜᴘs !", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
        st.status != enums.ChatMemberStatus.ADMINISTRATOR
        and st.status != enums.ChatMemberStatus.OWNER
        and str(userid) not in ADMINS
    ):
        return


    if len(args) < 2:
        await message.reply_text("Cᴏᴍᴍᴀɴᴅ Iɴᴄᴏᴍᴘʟᴇᴛᴇ :(", quote=True)
        return

    extracted = split_quotes(args[1])
    text = extracted[0].lower()

    if not message.reply_to_message and len(extracted) < 2:
        await message.reply_text("Aᴅᴅ Sᴏᴍᴇ Cᴏɴᴛᴇɴᴛ Tᴏ Sᴀᴠᴇ Yᴏᴜʀ Fɪʟᴛᴇʀ !", quote=True)
        return

    if (len(extracted) >= 2) and not message.reply_to_message:
        reply_text, btn, alert = parser(extracted[1], text, "alertmessage")
        fileid = None
        if not reply_text:
            await message.reply_text("Yᴏᴜ Cᴀɴɴᴏᴛ Hᴀᴠᴇ Bᴜᴛᴛᴏɴs Aʟᴏɴᴇ, Gɪᴠᴇ Sᴏᴍᴇ Tᴇxᴛ Tᴏ Gᴏ Wɪᴛʜ Iᴛ !", quote=True)
            return

    elif message.reply_to_message and message.reply_to_message.reply_markup:
        try:
            rm = message.reply_to_message.reply_markup
            btn = rm.inline_keyboard
            msg = get_file_id(message.reply_to_message)
            if msg:
                fileid = msg.file_id
                reply_text = message.reply_to_message.caption.html
            else:
                reply_text = message.reply_to_message.text.html
                fileid = None
            alert = None
        except:
            reply_text = ""
            btn = "[]" 
            fileid = None
            alert = None

    elif message.reply_to_message and message.reply_to_message.media:
        try:
            msg = get_file_id(message.reply_to_message)
            fileid = msg.file_id if msg else None
            reply_text, btn, alert = parser(extracted[1], text, "alertmessage") if message.reply_to_message.sticker else parser(message.reply_to_message.caption.html, text, "alertmessage")         
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    elif message.reply_to_message and message.reply_to_message.text:
        try:
            fileid = None
            reply_text, btn, alert = parser(message.reply_to_message.text.html, text, "alertmessage")
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    else:
        return

    await add_filter(grp_id, text, reply_text, btn, fileid, alert)

    await message.reply_text(
        f"Fɪʟᴛᴇʀ Fᴏʀ  `{text}`  Aᴅᴅᴇᴅ Iɴ  **{title}**",
        quote=True,
        parse_mode=enums.ParseMode.MARKDOWN
    )


@Client.on_message(filters.command(['viewfilters', 'filters']) & filters.incoming)
async def get_all(client, message):
    
    chat_type = message.chat.type
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"Yᴏᴜ Aʀᴇ Aɴᴏɴʏᴍᴏᴜs Aᴅᴍɪɴ. Usᴇ /connect {message.chat.id} Iɴ PM")
    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Mᴀᴋᴇ Sᴜʀᴇ I'ᴍ Pʀᴇsᴇɴᴛ Iɴ Yᴏᴜʀ Gʀᴏᴜᴘ !!", quote=True)
                return
        else:
            await message.reply_text("I'ᴍ Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ Aɴʏ Gʀᴏᴜᴘs !", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
        st.status != enums.ChatMemberStatus.ADMINISTRATOR
        and st.status != enums.ChatMemberStatus.OWNER
        and str(userid) not in ADMINS
    ):
        return

    texts = await get_filters(grp_id)
    count = await count_filters(grp_id)
    if count:
        filterlist = f"Tᴏᴛᴀʟ Nᴜᴍʙᴇʀ Oғ Fɪʟᴛᴇʀs Iɴ **{title}** : {count}\n\n"

        for text in texts:
            keywords = " ×  `{}`\n".format(text)

            filterlist += keywords

        if len(filterlist) > 4096:
            with io.BytesIO(str.encode(filterlist.replace("`", ""))) as keyword_file:
                keyword_file.name = "keywords.txt"
                await message.reply_document(
                    document=keyword_file,
                    quote=True
                )
            return
    else:
        filterlist = f"Tʜᴇʀᴇ Aʀᴇ Nᴏ Aᴄᴛɪᴠᴇ Fɪʟᴛᴇʀs Iɴ **{title}**"

    await message.reply_text(
        text=filterlist,
        quote=True,
        parse_mode=enums.ParseMode.MARKDOWN
    )
        
@Client.on_message(filters.command('del') & filters.incoming)
async def deletefilter(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"Yᴏᴜ Aʀᴇ Aɴᴏɴʏᴍᴏᴜs Aᴅᴍɪɴ. Usᴇ /connect {message.chat.id} Iɴ PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Mᴀᴋᴇ Sᴜʀᴇ I'ᴍ Pʀᴇsᴇɴᴛ Iɴ Yᴏᴜʀ Gʀᴏᴜᴘ !!", quote=True)
                return
        else:
            await message.reply_text("I'ᴍ Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ Aɴʏ Gʀᴏᴜᴘs !", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
        st.status != enums.ChatMemberStatus.ADMINISTRATOR
        and st.status != enums.ChatMemberStatus.OWNER
        and str(userid) not in ADMINS
    ):
        return

    try:
        cmd, text = message.text.split(" ", 1)
    except:
        await message.reply_text(
            "<i>Mᴇɴᴛɪᴏɴ Tʜᴇ Fɪʟᴛᴇʀɴᴀᴍᴇ Wʜɪᴄʜ Yᴏᴜ Wᴀɴɴᴀ Dᴇʟᴇᴛᴇ !</i>\n\n"
            "<code>/del Fɪʟᴛᴇʀɴᴀᴍᴇ</code>\n\n"
            "Use /viewfilters Tᴏ Vɪᴇᴡ Aʟʟ Aᴠᴀɪʟᴀʙʟᴇ Fɪʟᴛᴇʀs",
            quote=True
        )
        return

    query = text.lower()

    await delete_filter(message, query, grp_id)
        

@Client.on_message(filters.command('delall') & filters.incoming)
async def delallconfirm(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"Yᴏᴜ Aʀᴇ Aɴᴏɴʏᴍᴏᴜs Aᴅᴍɪɴ. Usᴇ /connect {message.chat.id} Iɴ PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Mᴀᴋᴇ Sᴜʀᴇ I'ᴍ Pʀᴇsᴇɴᴛ Iɴ Yᴏᴜʀ Gʀᴏᴜᴘ !!", quote=True)
                return
        else:
            await message.reply_text("I'ᴍ Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ Aɴʏ Gʀᴏᴜᴘs !", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return


    st = await client.get_chat_member(grp_id, userid)
    if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
        await message.reply_text(
            f"Tʜɪs Wɪʟʟ Dᴇʟᴇᴛᴇ Aʟʟ Fɪʟᴛᴇʀs Fʀᴏᴍ '{title}'.\nDᴏ Yᴏᴜ Wᴀɴᴛ Tᴏ Cᴏɴᴛɪɴᴜᴇ ??",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="Yᴇs",callback_data="delallconfirm")],
                [InlineKeyboardButton(text="Cᴀɴᴄᴇʟ",callback_data="delallcancel")]
            ]),
            quote=True
        )


# Kanged from https://github.com/KDBotz
@Client.on_message(filters.command(['gfilter', 'addg']) & filters.incoming & filters.user(ADMINS))
async def addgfilter(client, message):
    args = message.text.html.split(None, 1)

    if len(args) < 2:
        await message.reply_text("Cᴏᴍᴍᴀɴᴅ Iɴᴄᴏᴍᴘʟᴇᴛᴇ :(", quote=True)
        return

    extracted = split_quotes(args[1])
    text = extracted[0].lower()

    if not message.reply_to_message and len(extracted) < 2:
        await message.reply_text("Aᴅᴅ Sᴏᴍᴇ Cᴏɴᴛᴇɴᴛ Tᴏ Sᴀᴠᴇ Yᴏᴜʀ Fɪʟᴛᴇʀ !", quote=True)
        return

    if (len(extracted) >= 2) and not message.reply_to_message:
        reply_text, btn, alert = parser(extracted[1], text, "galert")
        fileid = None
        if not reply_text:
            await message.reply_text("Yᴏᴜ Cᴀɴɴᴏᴛ Hᴀᴠᴇ Bᴜᴛᴛᴏɴs Aʟᴏɴᴇ, Gɪᴠᴇ Sᴏᴍᴇ Tᴇxᴛ Tᴏ Gᴏ Wɪᴛʜ Iᴛ !", quote=True)
            return

    elif message.reply_to_message and message.reply_to_message.reply_markup:
        try:
            rm = message.reply_to_message.reply_markup
            btn = rm.inline_keyboard
            msg = get_file_id(message.reply_to_message)
            if msg:
                fileid = msg.file_id
                reply_text = message.reply_to_message.caption.html
            else:
                reply_text = message.reply_to_message.text.html
                fileid = None
            alert = None
        except:
            reply_text = ""
            btn = "[]" 
            fileid = None
            alert = None

    elif message.reply_to_message and message.reply_to_message.media:
        try:
            msg = get_file_id(message.reply_to_message)
            fileid = msg.file_id if msg else None
            reply_text, btn, alert = parser(extracted[1], text, "galert") if message.reply_to_message.sticker else parser(message.reply_to_message.caption.html, text, "galert")
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    elif message.reply_to_message and message.reply_to_message.text:
        try:
            fileid = None
            reply_text, btn, alert = parser(message.reply_to_message.text.html, text, "galert")
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    else:
        return

    await add_gfilter('gfilters', text, reply_text, btn, fileid, alert)

    await message.reply_text(
        f"GFilter for  `{text}`  added",
        quote=True,
        parse_mode=enums.ParseMode.MARKDOWN
    )


@Client.on_message(filters.command(['viewgfilters', 'gfilters']) & filters.incoming & filters.user(ADMINS))
async def get_all_gfilters(client, message):
    texts = await get_gfilters('gfilters')
    count = await count_gfilters('gfilters')
    if count:
        gfilterlist = f"Tᴏᴛᴀʟ Nᴜᴍʙᴇʀ Oғ gfilters : {count}\n\n"

        for text in texts:
            keywords = " ×  `{}`\n".format(text)

            gfilterlist += keywords

        if len(gfilterlist) > 4096:
            with io.BytesIO(str.encode(gfilterlist.replace("`", ""))) as keyword_file:
                keyword_file.name = "keywords.txt"
                await message.reply_document(
                    document=keyword_file,
                    quote=True
                )
            return
    else:
        gfilterlist = f"Tʜᴇʀᴇ Aʀᴇ Nᴏ Aᴄᴛɪᴠᴇ gfilters."

    await message.reply_text(
        text=gfilterlist,
        quote=True,
        parse_mode=enums.ParseMode.MARKDOWN
    )
        
@Client.on_message(filters.command('delg') & filters.incoming & filters.user(ADMINS))
async def deletegfilter(client, message):
    try:
        cmd, text = message.text.split(" ", 1)
    except:
        await message.reply_text(
            "<i>Mᴇɴᴛɪᴏɴ Tʜᴇ gfiltername Wʜɪᴄʜ Yᴏᴜ Wᴀɴɴᴀ Dᴇʟᴇᴛᴇ!</i>\n\n"
            "<code>/delg gfiltername</code>\n\n"
            "Use /viewgfilters Tᴏ Vɪᴇᴡ Aʟʟ Aᴠᴀɪʟᴀʙʟᴇ gfilters",
            quote=True
        )
        return

    query = text.lower()

    await delete_gfilter(message, query, 'gfilters')


@Client.on_message(filters.command('delallg') & filters.user(ADMINS))
async def delallgfill(client, message):
    await message.reply_text(
            f"Dᴏ Yᴏᴜ Wᴀɴᴛ Tᴏ Cᴏɴᴛɪɴᴜᴇ ??",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="Yᴇs",callback_data="gconforme")],
                [InlineKeyboardButton(text="Cᴀɴᴄᴇʟ",callback_data="close_data")]
            ]),
            quote=True
        )


@Client.on_callback_query(filters.regex("gconforme"))
async def dellacbd(client, message):
    await del_allg(message.message, 'gfilters')
    return await message.reply("👍 Dᴏɴᴇ")





