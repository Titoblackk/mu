from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from Music import app
from Music.MusicUtilities.tgcallsrun.music import pytgcalls as call_py

from Music.MusicUtilities.helpers.decorators import authorized_users_only
from Music.MusicUtilities.helpers.filters import command
from Music.MusicUtilities.tgcallsrun.queues import QUEUE, clear_queue
from Music.MusicUtilities.tgcallsrun.video import skip_current_song, skip_item


bttn = InlineKeyboardMarkup(
    [[InlineKeyboardButton("๐๏ธุฑุฌูููููููุน", callback_data="cbmenu")]]
)


bcl = InlineKeyboardMarkup([[InlineKeyboardButton("๐๏ธ ุงุบูุงู", callback_data="cls")]])


@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "Anda adalah **Admin Anonim** !\n\nยป kembali ke akun pengguna dari hak admin."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "๐ค ุงูุงุฏูู ููุท ูู ููููู ุงุณุชุฎุฏุงู ุงููุงุฆูู !",
            show_alert=True,
        )
    await query.edit_message_text(
        f"๐ ๏ธ **Pengaturan Dari** {query.message.chat.title}\n\n**โธ๏ธ : Jeda Streaming**\n**โถ๏ธ : Lanjutkan Streaming**\n**๐ : Bisukan Assistant**\n**๐ : Bunyikan Assistant**\n**โน๏ธ : Hentikan Streaming**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("โถ๏ธ", callback_data="cbstop"),
                    InlineKeyboardButton("โธ๏ธ", callback_data="cbpause"),
                    InlineKeyboardButton("โถ๏ธ", callback_data="cbresume"),
                ],
                [
                    InlineKeyboardButton("๐", callback_data="cbmute"),
                    InlineKeyboardButton("๐", callback_data="cbunmute"),
                ],
                [InlineKeyboardButton("๐๏ธ ุงุบูุงู", callback_data="cls")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "๐ก ุงูุงุฏูู ููุท ูู ููููู ุงุณุชุฎุฏุงู ุงููุงุฆูู !",
            show_alert=True,
        )
    await query.message.delete()


@app.on_message(command(["vskip"]) & filters.group)
@authorized_users_only
async def skip(client, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="๐ฐ๏ธุงููุงุฆูู", callback_data="cbmenu"),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("โ Tidak ada yang sedang diputar")
        elif op == 1:
            await m.reply(
                "๐ **Antrian Sedang Kosong.**\n\n**โข Assistant Meninggalkan Obrolan Suara**"
            )
        elif op == 2:
            await m.reply(
                "๐๏ธ **Membersihkan Antrian**\n\n**โข Assistant Meninggalkan Obrolan Suara**"
            )
        else:
            await m.reply(
                f"""
โญ๏ธ **Memutar {op[2]} Selanjutnya**
๐ท **Nama:** [{op[0]}]({op[1]})
๐๐ปโโ๏ธ **Atas permintaan:** {m.from_user.mention()}
""",
                disable_web_page_preview=True,
                reply_markup=keyboard,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "๐ **Lagu dihapus dari antrian:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@app.on_message(command(["vstop","vend"]) & filters.group)
@authorized_users_only
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("โ **Streaming telah berakhir.**")
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("โ **Tidak ada dalam streaming**")


@app.on_message(command(["vpause"]) & filters.group)
@authorized_users_only
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                "โธ๏ธ **Video dijeda.**\n\nโข **Untuk melanjutkan video, gunakan Perintah** ยป /vresume"
            )
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("โ **Tidak ada dalam streaming**")


@app.on_message(command(["vresume"]) & filters.group)
@authorized_users_only
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                "โท **Video dilanjutkan.**\n\nโข **Untuk menjeda video, gunakan Perintah** ยป /vpause"
            )
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("โ **Tidak ada dalam streaming**")


@app.on_message(command(["vmute"]) & filters.group)
@authorized_users_only
async def mute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await m.reply(
                "๐ **Assistant dibisukan.**\n\nโข **Untuk mengaktifkan suara Assistant, gunakan Perintah**\nยป /vunmute"
            )
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("โ **Tidak ada dalam streaming**")


@app.on_message(command(["vunmute"]) & filters.group)
@authorized_users_only
async def unmute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await m.reply(
                "๐ **Assistant diaktifkan.**\n\nโข **Untuk menonaktifkan bot pengguna, gunakan Perintah**\nยป /vmute"
            )
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("โ **Tidak ada dalam streaming**")


@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "Anda adalah **Admin Anonim** !\n\nยป kembali ke akun pengguna dari hak admin."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "๐ก ุงูุงุฏูู ููุท ูู ููููู ุงุณุชุฎุฏุงู ุงููุงุฆูู!",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await query.edit_message_text("II Streaming telah dijeda", reply_markup=bttn)
        except Exception as e:
            await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("โ Tidak ada yang sedang streaming", show_alert=True)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "Anda adalah **Admin Anonim** !\n\nยป kembali ke akun pengguna dari hak admin."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "๐ก ุงูุงุฏูู ููุท ูู ููููู ุงุณุชุฎุฏุงู ุงููุงุฆูู !",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await query.edit_message_text(
                "**โถ๏ธ Streaming telah dilanjutkan**", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("โ Tidak ada yang sedang streaming", show_alert=True)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "Anda adalah **Admin Anonim** !\n\nยป kembali ke akun pengguna dari hak admin."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "๐ก ุงูุงุฏูู ููุท ูู ููููู ุงุณุชุฎุฏุงู ุงููุงุฆูู !",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text(
                "โ **Streaming telah berakhir**", reply_markup=bcl
            )
        except Exception as e:
            await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("โ Tidak ada yang sedang streaming", show_alert=True)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "Anda adalah **Admin Anonim** !\n\nยป kembali ke akun pengguna dari hak admin."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "๐ก ุงูุงุฏูู ููุท ูู ููููู ุงุณุชุฎุฏุงู ุงููุงุฆูู !",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await query.edit_message_text(
                "๐ Assistant berhasil dimatikan", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"***Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("โ Tidak ada yang sedang streaming", show_alert=True)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "Anda adalah **Admin Anonim** !\n\nยป kembali ke akun pengguna dari hak admin."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "๐ก ุงูุงุฏูู ููุท ูู ููููู ุงุณุชุฎุฏุงู ุงููุงุฆูู !",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await query.edit_message_text(
                "๐ Assistant berhasil dibunyikan", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("โ Tidak ada yang sedang streaming", show_alert=True)


@app.on_message(command(["volume", "vol"]))
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(range))
            await m.reply(f"โ **Volume Disetel Ke** `{range}`%")
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("โ **Tidak ada dalam streaming**")
