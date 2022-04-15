from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
from asyncio import QueueEmpty
from pyrogram import Client, filters
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream
from Music import app, BOT_USERNAME, dbb, SUDOERS
import os
import yt_dlp
from youtubesearchpython import VideosSearch
from Music.config import LOG_GROUP_ID
from Music.config import GROUP, CHANNEL, BOT_IMG, OWNER_USERNAME, MOT_IMG, HANNEL, ROUP, OT_IMG
from Music.MusicUtilities.tgcallsrun import ASS_ACC
from os import path
import random
import time as sedtime 
import asyncio
import shutil
from time import time
from Music import converter
import aiohttp
from aiohttp import ClientResponseError, ServerTimeoutError, TooManyRedirects
from Music import dbb, app, BOT_USERNAME, BOT_ID, ASSID, ASSNAME, ASSUSERNAME, ASSMENTION
from Music.MusicUtilities.tgcallsrun import (music, convert, download, clear, get, is_empty, put, task_done, smexy)
from Music.MusicUtilities.helpers.decorators import errors
from Music.MusicUtilities.helpers.filters import command, other_filters
from Music.MusicUtilities.helpers.paste import paste
from Music.MusicUtilities.tgcallsrun import (music, clear, get, is_empty, put, task_done)
from Music.MusicUtilities.database.queue import (is_active_chat, add_active_chat, remove_active_chat, music_on, is_music_playing, music_off)
from Music.MusicUtilities.database.playlist import (get_playlist_count, _get_playlists, get_note_names, get_playlist, save_playlist, delete_playlist)
from Music.MusicUtilities.database.assistant import (_get_assistant, get_assistant, save_assistant)
from Music.MusicUtilities.helpers.inline import (play_keyboard, search_markup, play_markup, playlist_markup, audio_markup)
from Music.MusicUtilities.helpers.inline import play_keyboard, confirm_keyboard, play_list_keyboard, close_keyboard, confirm_group_keyboard
from Music.MusicUtilities.tgcallsrun import (music, convert, download, clear, get, is_empty, put, task_done, smexy)
from Music.MusicUtilities.database.queue import (is_active_chat, add_active_chat, remove_active_chat, music_on, is_music_playing, music_off)
from Music.MusicUtilities.database.onoff import (is_on_off, add_on, add_off)
from Music.MusicUtilities.database.blacklistchat import (blacklisted_chats, blacklist_chat, whitelist_chat)
from Music.MusicUtilities.database.gbanned import (get_gbans_count, is_gbanned_user, add_gban_user, add_gban_user)
from Music.MusicUtilities.database.theme import (_get_theme, get_theme, save_theme)
from Music.MusicUtilities.database.assistant import (_get_assistant, get_assistant, save_assistant)
from Music.config import DURATION_LIMIT, ASS_ID
from Music.MusicUtilities.helpers.decorators import errors
from Music.MusicUtilities.helpers.filters import command
from Music.MusicUtilities.helpers.gets import (get_url, themes, random_assistant, ass_det)
from Music.MusicUtilities.helpers.thumbnails import gen_thumb
from Music.MusicUtilities.helpers.chattitle import CHAT_TITLE
from Music.MusicUtilities.helpers.ytdl import ytdl_opts 
from Music.MusicUtilities.helpers.inline import (play_keyboard, search_markup, play_markup, playlist_markup)
import requests
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
import re
import aiofiles
from pykeyboard import InlineKeyboard
from pyrogram import filters
from Music import aiohttpsession as session

pattern = re.compile(
    r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$"
)

flex = {}

async def isPreviewUp(preview: str) -> bool:
    for _ in range(7):
        try:
            async with session.head(preview, timeout=2) as resp:
                status = resp.status
                size = resp.content_length
        except asyncio.exceptions.TimeoutError:
            return False
        if status == 404 or (status == 200 and size == 0):
            await asyncio.sleep(0.4)
        else:
            return True if status == 200 else False
    return False


    
@Client.on_callback_query(filters.regex(pattern=r"ppcl"))
async def closesmex(_,CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    chat_id = CallbackQuery.message.chat.id
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id 
    try:
        smex, user_id = callback_request.split("|") 
    except Exception as e:
        await CallbackQuery.message.edit(f"Error Occured\n**Possible reason could be**:{e}")
        return 
    if CallbackQuery.from_user.id != int(user_id):
        await CallbackQuery.answer("لا يسمح لك بإغلاق القائمة", show_alert=True)
        return
    await CallbackQuery.message.delete()
    await CallbackQuery.answer()
    
    
@Client.on_callback_query(filters.regex("pausevc"))
async def pausevc(_,CallbackQuery):
    a = await app.get_chat_member(CallbackQuery.message.chat.id , CallbackQuery.from_user.id)
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer("ليس لديك إذن مطلوب لأداء هذا الإجراء.\nPermission: MANAGE VOICE CHATS", show_alert=True)
    checking = CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await music.pytgcalls.pause_stream(chat_id)
            await music_off(chat_id)
            await CallbackQuery.answer("وقف", show_alert=True)
            user_id = CallbackQuery.from_user.id
            user_name = CallbackQuery.from_user.first_name
            rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"
            await CallbackQuery.message.reply(f"**🎧 Voicechat Paused By User {rpk}!**", reply_markup=play_keyboard)
            await CallbackQuery.message.delete()
        else:
            await CallbackQuery.answer(f"ليس هناك موسيقي جاريه!", show_alert=True)
            return
    else:
        await CallbackQuery.answer(f"ليس هناك موسيقي جاريه!", show_alert=True)
   
    
@Client.on_callback_query(filters.regex("resumevc"))
async def resumevc(_,CallbackQuery):  
    a = await app.get_chat_member(CallbackQuery.message.chat.id , CallbackQuery.from_user.id)
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer("ليس لديك إذن مطلوب لأداء هذا الإجراء.\nPermission: MANAGE VOICE CHATS", show_alert=True)
    checking = CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await CallbackQuery.answer("لا أعتقد إذا توقف شيء ما على الدردشة الصوتية", show_alert=True)
            return    
        else:
            await music_on(chat_id)
            await music.pytgcalls.resume_stream(chat_id)
            await CallbackQuery.answer("تخطي", show_alert=True)
            user_id = CallbackQuery.from_user.id
            user_name = CallbackQuery.from_user.first_name
            rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"
            await CallbackQuery.message.reply(f"**🎧 تم تخطي الاغنيه بواسطة {rpk}!**", reply_markup=play_keyboard)
            await CallbackQuery.message.delete()
    else:
        await CallbackQuery.answer(f"ليس هناك موسيقي جاريه!", show_alert=True)
   
    
@Client.on_callback_query(filters.regex("skipvc"))
async def skipvc(_,CallbackQuery): 
    a = await app.get_chat_member(CallbackQuery.message.chat.id , CallbackQuery.from_user.id)
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer("ليس لديك إذن مطلوب لأداء هذا الإجراء.\nPermission: MANAGE VOICE CHATS", show_alert=True)
    checking = CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    chat_title = CallbackQuery.message.chat.title
    if await is_active_chat(chat_id):
        task_done(chat_id)
        if is_empty(chat_id):
            user_id = CallbackQuery.from_user.id
            await remove_active_chat(chat_id) 
            user_name = CallbackQuery.from_user.first_name
            rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"
            await remove_active_chat(chat_id)
            await CallbackQuery.answer()
            await CallbackQuery.message.reply(f"**⛔️ Skip Button Used By {rpk}**\n\n**🤦‍♂ No More Music In** __Queues__ \n\n**📨 Leaving Voice Chat Now..**")
            await music.pytgcalls.leave_group_call(chat_id)
            return
        else:
            await CallbackQuery.answer("📨 Voicechat Skipped", show_alert=True)
            afk = get(chat_id)['file']
            f1 = (afk[0])
            f2 = (afk[1])
            f3 = (afk[2])
            finxx = (f"{f1}{f2}{f3}")
            if str(finxx) != "raw":   
                mystic = await CallbackQuery.message.reply("Music Is Currently Playing Playlist...\n\nDownloading Next Music From Playlist....")
                url = (f"https://www.youtube.com/watch?v={afk}")
                try:
                    with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                        x = ytdl.extract_info(url, download=False)
                except Exception as e:
                    return await mystic.edit(f"Failed to download this video.\n\n**Reason**:{e}") 
                title = (x["title"])
                videoid = afk
                def my_hook(d):
                    if d['status'] == 'تنزيل':
                        percentage = d['_percent_str']
                        per = (str(percentage)).replace(".","", 1).replace("%","", 1)
                        per = int(per)
                        eta = d['eta']
                        speed = d['_speed_str']
                        size = d['_total_bytes_str']
                        bytesx = d['total_bytes']
                        if str(bytesx) in flex:
                            pass
                        else:
                            flex[str(bytesx)] = 1
                        if flex[str(bytesx)] == 1:
                            flex[str(bytesx)] += 1
                            sedtime.sleep(1)
                            mystic.edit(f"Downloading {title[:50]}\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                        if per > 500:    
                            if flex[str(bytesx)] == 2:
                                flex[str(bytesx)] += 1
                                sedtime.sleep(0.5)
                                mystic.edit(f"Downloading {title[:50]}...\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} in {chat_title} | ETA: {eta} seconds")
                        if per > 800:    
                            if flex[str(bytesx)] == 3:
                                flex[str(bytesx)] += 1
                                sedtime.sleep(0.5)
                                mystic.edit(f"Downloading {title[:50]}....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} in {chat_title} | ETA: {eta} seconds")
                        if per == 1000:    
                            if flex[str(bytesx)] == 4:
                                flex[str(bytesx)] = 1
                                sedtime.sleep(0.5)
                                mystic.edit(f"Downloading {title[:50]}.....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec") 
                                print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} in {chat_title} | ETA: {eta} seconds")
                loop = asyncio.get_event_loop()
                xx = await loop.run_in_executor(None, download, url, my_hook)
                file = await convert(xx)
                await music.pytgcalls.change_stream(
                    chat_id, 
                    InputStream(
                        InputAudioStream(
                            file,
                        ),
                    ),
                )
                thumbnail = (x["thumbnail"])
                duration = (x["duration"])
                duration = round(x["duration"] / 60)
                theme = random.choice(themes)
                ctitle = (await app.get_chat(chat_id)).title
                ctitle = await CHAT_TITLE(ctitle)
                f2 = open(f'search/{afk}id.txt', 'r')        
                userid =(f2.read())
                thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)
                user_id = userid
                buttons = play_markup(videoid, user_id)
                await mystic.delete()
                semx = await app.get_users(userid)
                user_id = CallbackQuery.from_user.id
                user_name = CallbackQuery.from_user.first_name
                rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"
                await CallbackQuery.message.reply_photo(
                photo= thumb,
                reply_markup=InlineKeyboardMarkup(buttons),    
                caption=(f"<b>__Skipped Voice Chat By {rpk}__</b>\n\n🎥<b>__Started Playing:__ </b>[{title[:25]}]({url}) \n⏳<b>__Duration:__</b> {duration} Mins\n👤**__Requested by:__** {semx.mention}")
            )   
                os.remove(thumb)
            else:      
                await music.pytgcalls.change_stream(
                    chat_id, 
                    InputStream(
                        InputAudioStream(
                            afk,
                        ),
                    ),
                )
                _chat_ = ((str(afk)).replace("_","", 1).replace("/","", 1).replace(".","", 1))
                f2 = open(f'search/{_chat_}title.txt', 'r')        
                title =(f2.read())
                f3 = open(f'search/{_chat_}duration.txt', 'r')        
                duration =(f3.read())
                f4 = open(f'search/{_chat_}username.txt', 'r')        
                username =(f4.read())
                f4 = open(f'search/{_chat_}videoid.txt', 'r')        
                videoid =(f4.read())
                user_id = 1
                videoid = str(videoid)
                if videoid == "smex1":
                    buttons = audio_markup(videoid, user_id)
                else:
                    buttons = play_markup(videoid, user_id)
                user_id = CallbackQuery.from_user.id
                user_name = CallbackQuery.from_user.first_name
                rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"    
                await CallbackQuery.message.reply_photo(
                photo=f"downloads/{_chat_}final.png",
                reply_markup=InlineKeyboardMarkup(buttons),
                caption=f"<b>__Skipped Voice Chat By {rpk}__</b>\n\n🎥<b>__Started Playing:__</b> {title} \n⏳<b>__Duration:__</b> {duration} \n👤<b>__Requested by:__ </b> {username}",
                )
                return
            
            
       
@Client.on_callback_query(filters.regex("stopvc"))
async def stopvc(_,CallbackQuery):
    a = await app.get_chat_member(CallbackQuery.message.chat.id , CallbackQuery.from_user.id)
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer("ليس لديك إذن مطلوب لأداء هذا الإجراء.\nPermission: MANAGE VOICE CHATS", show_alert=True)
    checking = CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        try:
            clear(chat_id)
        except QueueEmpty:
            pass
        try:
            await music.pytgcalls.leave_group_call(chat_id)
        except Exception as e:
            pass
        await remove_active_chat(chat_id) 
        await CallbackQuery.answer("انهي", show_alert=True)
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"
        await CallbackQuery.message.reply(f"**🎧 Voicechat End/Stopped By {rpk}!**")
    else:
        await CallbackQuery.answer(f"**ليس هناك موسيقي جاريه!**", show_alert=True)

        
@Client.on_callback_query(filters.regex("play_playlist"))
async def play_playlist(_,CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    chat_id = CallbackQuery.message.chat.id
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id 
    try:
        user_id,smex = callback_request.split("|") 
    except Exception as e:
        await CallbackQuery.answer()
        return await CallbackQuery.message.edit(f"Error Occured\n**Possible reason could be**:{e}")
    Name = CallbackQuery.from_user.first_name
    chat_title = CallbackQuery.message.chat.title
    if str(smex) == "personal":
        if CallbackQuery.from_user.id != int(user_id):
            return await CallbackQuery.answer("This Is Not Forr You! Play Your Own Playlist Stupid!", show_alert=True)
        _playlist = await get_note_names(userid)
        if not _playlist:
            return await CallbackQuery.answer(f"You Have No Playlist On Servers.", show_alert=True)
        else:
            await CallbackQuery.message.delete()
            logger_text=f"""Starting Playlist

Group :- {chat_title}
By :- {Name}

Personal Playlist Playing."""
            await ASS_ACC.send_message(LOG_GROUP_ID, f"{logger_text}", disable_web_page_preview=True)
            mystic = await CallbackQuery.message.reply_text(f"Starting {Name}'s Personal Playlist.\n\nRequested By:- {CallbackQuery.from_user.first_name}")   
            checking = f"[{CallbackQuery.from_user.first_name}](tg://user?id={userid})"
            msg = f"Queued Playlist:\n\n"
            j = 0
            for note in _playlist:
                _note = await get_playlist(CallbackQuery.from_user.id, note)
                title = _note["title"]
                videoid = _note["videoid"]
                url = (f"https://www.youtube.com/watch?v={videoid}")
                duration = _note["duration"]
                if await is_active_chat(chat_id):
                    position = await put(chat_id, file=videoid)
                    j += 1
                    msg += f"{j}- {title[:50]}\n"
                    msg += f"   Queued Position- {position}\n\n"
                    f20 = open(f'search/{videoid}id.txt', 'w')
                    f20.write(f"{user_id}") 
                    f20.close()
                else:
                    try:
                        with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                            x = ytdl.extract_info(url, download=False)
                    except Exception as e:
                        return await mystic.edit(f"Failed to download this video.\n\n**Reason**:{e}") 
                    title = (x["title"])
                    thumbnail = (x["thumbnail"])
                    def my_hook(d): 
                        if d['status'] == 'downloading':
                            percentage = d['_percent_str']
                            per = (str(percentage)).replace(".","", 1).replace("%","", 1)
                            per = int(per)
                            eta = d['eta']
                            speed = d['_speed_str']
                            size = d['_total_bytes_str']
                            bytesx = d['total_bytes']
                            if str(bytesx) in flex:
                                pass
                            else:
                                flex[str(bytesx)] = 1
                            if flex[str(bytesx)] == 1:
                                flex[str(bytesx)] += 1
                                try:
                                    if eta > 2:
                                        mystic.edit(f"Downloading {title[:50]}\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                except Exception as e:
                                    pass
                            if per > 250:    
                                if flex[str(bytesx)] == 2:
                                    flex[str(bytesx)] += 1
                                    if eta > 2:     
                                        mystic.edit(f"Downloading {title[:50]}..\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                    print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds")
                            if per > 500:    
                                if flex[str(bytesx)] == 3:
                                    flex[str(bytesx)] += 1
                                    if eta > 2:     
                                        mystic.edit(f"Downloading {title[:50]}...\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                    print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds")
                            if per > 800:    
                                if flex[str(bytesx)] == 4:
                                    flex[str(bytesx)] += 1
                                    if eta > 2:    
                                        mystic.edit(f"Downloading {title[:50]}....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                    print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds")
                        if d['status'] == 'finished': 
                            try:
                                taken = d['_elapsed_str']
                            except Exception as e:
                                taken = "00:00"
                            size = d['_total_bytes_str']
                            mystic.edit(f"**Downloaded {title[:50]}.....**\n\n**FileSize:** {size}\n**Time Taken:** {taken} sec\n\n**Converting File**[__FFmpeg processing__]")
                            print(f"[{videoid}] Downloaded| Elapsed: {taken} seconds")  
                    loop = asyncio.get_event_loop()
                    xx = await loop.run_in_executor(None, download, url, my_hook)
                    file = await convert(xx)
                    await music_on(chat_id)
                    await add_active_chat(chat_id)
                    await music.pytgcalls.join_group_call(
                        chat_id, 
                        InputStream(
                            InputAudioStream(
                                file,
                            ),
                        ),
                        stream_type=StreamType().local_stream,
                    )
                    theme = random.choice(themes)
                    ctitle = CallbackQuery.message.chat.title
                    ctitle = await CHAT_TITLE(ctitle)
                    thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)  
                    buttons = play_markup(videoid, user_id)
                    m = await CallbackQuery.message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),    
                    caption=(f"🎥<b>__Playing:__ </b>[{title[:25]}]({url}) \n⏳<b>__Duration:__</b> {duration} \n💡<b>__Info:__</b> [Get Additional Information](https://t.me/{BOT_USERNAME}?start=info_{videoid})\n👤**__Requested by:__** {checking}")
                )   
                    os.remove(thumb)
                    await CallbackQuery.message.delete()
        await mystic.delete()
        m = await CallbackQuery.message.reply_text("Pasting Queued Playlist to Bin")
        link = await paste(msg)
        preview = link + "/preview.png"
        urlxp = link + "/index.txt"
        a1 = InlineKeyboardButton(text=f"تسجيل الخروج قائمة التشغيل", url=urlxp)
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="▶️", callback_data=f'resumevc'),
                    InlineKeyboardButton(text="⏸️", callback_data=f'pausevc'),
                    InlineKeyboardButton(text="⏭️", callback_data=f'skipvc'),
                    InlineKeyboardButton(text="⏹️", callback_data=f'stopvc')
                ],
                [
                    a1,
                ],
                [
                    InlineKeyboardButton(text="🗑 إغلاق القائمة", callback_data=f'close2')
                ]    
            ]
        )
        if await isPreviewUp(preview):
            try:
                await CallbackQuery.message.reply_photo(
                    photo=preview, caption=f"This is Queued Playlist Of {Name}.\n\nIf you want to delete any music from playlist use : /delmyplaylist", quote=False, reply_markup=key
                )
                await m.delete()
            except Exception:
                pass
        else:
            await CallbackQuery.message.reply_text(
                    text=msg, reply_markup=key
                )
            await m.delete()
    if str(smex) == "group":
        _playlist = await get_note_names(CallbackQuery.message.chat.id)
        if not _playlist:
            return await CallbackQuery.answer(f"Your Group Has No Playlist On Servers. Try Adding Musics In Playlist.", show_alert=True)
        else:
            await CallbackQuery.message.delete()
            logger_text=f"""Starting Playlist

Group :- {chat_title}
By :- {Name}

Group Playlist Playing."""
            await ASS_ACC.send_message(LOG_GROUP_ID, f"{logger_text}", disable_web_page_preview=True)
            mystic = await CallbackQuery.message.reply_text(f"Starting Groups's Playlist.\n\nRequested By:- {CallbackQuery.from_user.first_name}")   
            checking = f"[{CallbackQuery.from_user.first_name}](tg://user?id={userid})"
            msg = f"Queued Playlist:\n\n"
            j = 0
            for note in _playlist:
                _note = await get_playlist(CallbackQuery.message.chat.id, note)
                title = _note["title"]
                videoid = _note["videoid"]
                url = (f"https://www.youtube.com/watch?v={videoid}")
                duration = _note["duration"]
                if await is_active_chat(chat_id):
                    position = await put(chat_id, file=videoid)
                    j += 1
                    msg += f"{j}- {title[:50]}\n"
                    msg += f"   Queued Position- {position}\n\n"
                    f20 = open(f'search/{videoid}id.txt', 'w')
                    f20.write(f"{user_id}") 
                    f20.close()
                else:
                    try:
                        with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                            x = ytdl.extract_info(url, download=False)
                    except Exception as e:
                        return await mystic.edit(f"Failed to download this video.\n\n**Reason**:{e}") 
                    title = (x["title"])
                    thumbnail = (x["thumbnail"])
                    def my_hook(d): 
                        if d['status'] == 'downloading':
                            percentage = d['_percent_str']
                            per = (str(percentage)).replace(".","", 1).replace("%","", 1)
                            per = int(per)
                            eta = d['eta']
                            speed = d['_speed_str']
                            size = d['_total_bytes_str']
                            bytesx = d['total_bytes']
                            if str(bytesx) in flex:
                                pass
                            else:
                                flex[str(bytesx)] = 1
                            if flex[str(bytesx)] == 1:
                                flex[str(bytesx)] += 1
                                try:
                                    if eta > 2:
                                        mystic.edit(f"Downloading {title[:50]}\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                except Exception as e:
                                    pass
                            if per > 250:    
                                if flex[str(bytesx)] == 2:
                                    flex[str(bytesx)] += 1
                                    if eta > 2:     
                                        mystic.edit(f"Downloading {title[:50]}..\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                    print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds")
                            if per > 500:    
                                if flex[str(bytesx)] == 3:
                                    flex[str(bytesx)] += 1
                                    if eta > 2:     
                                        mystic.edit(f"Downloading {title[:50]}...\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                    print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds")
                            if per > 800:    
                                if flex[str(bytesx)] == 4:
                                    flex[str(bytesx)] += 1
                                    if eta > 2:    
                                        mystic.edit(f"Downloading {title[:50]}....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                    print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds")
                        if d['status'] == 'finished': 
                            try:
                                taken = d['_elapsed_str']
                            except Exception as e:
                                taken = "00:00"
                            size = d['_total_bytes_str']
                            mystic.edit(f"**📥 Downloaded {title[:50]}.....**\n\n**📚 FileSize:** {size}\n**⚡ Time Taken:** {taken} sec\n\n**📑 Converting Flicks File**")
                            print(f"[{videoid}] Downloaded| Elapsed: {taken} seconds")  
                    loop = asyncio.get_event_loop()
                    xx = await loop.run_in_executor(None, download, url, my_hook)
                    file = await convert(xx)
                    await music_on(chat_id)
                    await add_active_chat(chat_id)
                    await music.pytgcalls.join_group_call(
                        chat_id, 
                        InputStream(
                            InputAudioStream(
                                file,
                            ),
                        ),
                        stream_type=StreamType().local_stream,
                    )
                    theme = random.choice(themes)
                    ctitle = CallbackQuery.message.chat.title
                    ctitle = await CHAT_TITLE(ctitle)
                    thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)
                    buttons = play_markup(videoid, user_id)
                    m = await CallbackQuery.message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),    
                    caption=(f"🎥<b>__Playing:__ </b>[{title[:25]}]({url}) \n⏳<b>__Duration:__</b> {duration} \n⚡<b>__Info:__</b> [Get Additional Information](https://t.me/{BOT_USERNAME}?start=info_{videoid})\n👤**__Requested by:__** {checking}")
                )   
                    os.remove(thumb)
                    await CallbackQuery.message.delete()
        await asyncio.sleep(1)
        await mystic.delete()
        m = await CallbackQuery.message.reply_text("Pasting Queued Playlist to Bin")
        link = await paste(msg)
        preview = link + "/preview.png"
        urlxp = link + "/index.txt"
        a1 = InlineKeyboardButton(text=f"تسجيل الخروج قائمة التشغيل", url=urlxp)
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="▶️", callback_data=f'resumevc'),
                    InlineKeyboardButton(text="⏸️", callback_data=f'pausevc'),
                    InlineKeyboardButton(text="⏭️", callback_data=f'skipvc'),
                    InlineKeyboardButton(text="⏹️", callback_data=f'stopvc')
                ],
                [
                    a1,
                ],
                [
                    InlineKeyboardButton(text="🗑 إغلاق القائمة", callback_data=f'close2')
                ]    
            ]
        )
        if await isPreviewUp(preview):
            try:
                await CallbackQuery.message.reply_photo(
                    photo=preview, caption=f"This is Queued Playlist of Your Group.\n\nIf you want to delete any music from playlist use : /delgroupplaylist", quote=False, reply_markup=key
                )
                await m.delete()
            except Exception:
                pass
        else:
            await CallbackQuery.message.reply_text(
                    text=msg, reply_markup=key
                )
            await m.delete()
 
@Client.on_callback_query(filters.regex("group_playlist"))
async def group_playlist(_,CallbackQuery):
    await CallbackQuery.answer()
    a = await app.get_chat_member(CallbackQuery.message.chat.id , CallbackQuery.from_user.id)
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer("ليس لديك إذن مطلوب لأداء هذا الإجراء.\nPermission: MANAGE VOICE CHATS", show_alert=True)
    callback_data = CallbackQuery.data.strip()
    chat_id = CallbackQuery.message.chat.id
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id 
    try:
        url,smex= callback_request.split("|") 
    except Exception as e:
        return await CallbackQuery.message.edit(f"Error Occured\n**Possible reason could be**: {e}")
    Name = CallbackQuery.from_user.first_name
    _count = await get_note_names(chat_id)
    count = 0
    if not _count:
        sex = await CallbackQuery.message.reply_text("Welcome To Music's Playlist Feature.\n\nGenerating Your Group's Playlist In Database...Please wait.")
        await asyncio.sleep(2)
        await sex.delete()
    else:
        for smex in _count:
            count += 1   
    count = int(count)
    if count == 30:
        return await CallbackQuery.message.reply_text("Sorry! You can only have 30 music in group playlist.")
    try:
        url = (f"https://www.youtube.com/watch?v={url}")
        results = VideosSearch(url, limit=1)
        for result in results.result()["result"]:
            title = (result["title"])
            duration = (result["duration"])
            videoid = (result["id"])
    except Exception as e:
            return await CallbackQuery.message.reply_text(f"Some Error Occured.\n**Possible Reason:** {e}") 
    _check = await get_playlist(chat_id, videoid)
    title = title[:50]
    if _check:
         return await CallbackQuery.message.reply_text(f"{Name}, Its already in the Playlist!")   
    assis = {
        "videoid": videoid,
        "title": title,
        "duration": duration,
    }
    await save_playlist(chat_id, videoid, assis)
    Name = CallbackQuery.from_user.first_name
    return await CallbackQuery.message.reply_text(f"Added to Group's Playlist by {Name}")
  

@Client.on_callback_query(filters.regex("playlist"))
async def pla_playylistt(_,CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    chat_id = CallbackQuery.message.chat.id
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id 
    try:
        url,smex= callback_request.split("|") 
    except Exception as e:
        return await CallbackQuery.message.edit(f"Error Occured\n**Possible reason could be**:{e}")
    Name = CallbackQuery.from_user.first_name
    _count = await get_note_names(userid)
    count = 0
    if not _count:
        sex = await CallbackQuery.message.reply_text("**Welcome To Music's Playlist Feature.**\n\n**Generating Your Playlist In Database...Please wait.**")
        await asyncio.sleep(2)
        await sex.delete()
    else:
        for smex in _count:
            count += 1   
    count = int(count)
    if count == 30:
        if userid in SUDOERS:
            pass
        else:
            return await CallbackQuery.message.reply_text("Sorry! You can only have 30 music in your playlist.")
    try:
        url = (f"https://www.youtube.com/watch?v={url}")
        results = VideosSearch(url, limit=1)
        for result in results.result()["result"]:
            title = (result["title"])
            duration = (result["duration"])
            videoid = (result["id"])
    except Exception as e:
            return await CallbackQuery.message.reply_text(f"Some Error Occured.\n**Possible Reason:**{e}") 
    _check = await get_playlist(userid, videoid)
    if _check:
         return await CallbackQuery.message.reply_text(f"{Name}, Its already in the Playlist!") 
    title = title[:50]    
    assis = {
        "videoid": videoid,
        "title": title,
        "duration": duration,
    }
    await save_playlist(userid, videoid, assis)
    return await CallbackQuery.message.reply_text(f"Added to {Name}'s Playlist")   
    
    

@Client.on_callback_query(filters.regex("P_list"))
async def P_list(_,CallbackQuery):
    _playlist = await get_note_names(CallbackQuery.from_user.id)
    if not _playlist:
        return await CallbackQuery.answer(f"You have no Personal Playlist on servers. Try adding musics in playlist.", show_alert=True)
    else:
        j = 0
        await CallbackQuery.answer()
        msg = f"Personal Playlist:\n\n"
        for note in _playlist:
            j += 1
            _note = await get_playlist(CallbackQuery.from_user.id, note)
            title = _note["title"]
            duration = _note["duration"]
            msg += f"{j}- {title[:60]}\n"
            msg += f"    Duration- {duration} Min(s)\n\n"   
        await CallbackQuery.answer()
        await CallbackQuery.message.delete()     
        m = await CallbackQuery.message.reply_text("Pasting Playlist to Bin")
        link = await paste(msg)
        preview = link + "/preview.png"
        print(link)
        urlxp = link + "/index.txt"
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        a2 = InlineKeyboardButton(text=f"Play {user_name[:17]}'s Playlist", callback_data=f'play_playlist {user_id}|personal')
        a3 = InlineKeyboardButton(text=f"📨 تحقق من قائمة التشغيل", url=urlxp)
        key = InlineKeyboardMarkup(
            [
                [
                    a2,
                ],
                [
                    a3,
                    InlineKeyboardButton(text="🗑 إغلاق القائمة", callback_data=f'close2')
                ]    
            ]
        )
        if await isPreviewUp(preview):
            try:
                await CallbackQuery.message.reply_photo(
                    photo=preview, quote=False, reply_markup=key
                )
                await m.delete()
            except Exception as e :
                print(e)
                pass
        else:
            print("5")
            await CallbackQuery.message.reply_photo(
                    photo=link, quote=False, reply_markup=key
                )
            await m.delete()
    
    
@Client.on_callback_query(filters.regex("G_list"))
async def G_list(_,CallbackQuery):
    user_id = CallbackQuery.from_user.id
    _playlist = await get_note_names(CallbackQuery.message.chat.id)
    if not _playlist:
        return await CallbackQuery.answer(f"You have no Group Playlist on servers. Try adding musics in playlist.", show_alert=True)
    else:
        await CallbackQuery.answer()
        j = 0
        msg = f"Group Playlist:\n\n"
        for note in _playlist:
            j += 1
            _note = await get_playlist(CallbackQuery.message.chat.id, note)
            title = _note["title"]
            duration = _note["duration"]
            msg += f"{j}- {title[:60]}\n"
            msg += f"    Duration- {duration} Min(s)\n\n"
        await CallbackQuery.answer()
        await CallbackQuery.message.delete()
        m = await CallbackQuery.message.reply_text("Pasting Playlist to Bin")
        link = await paste(msg)
        preview = link + "/preview.png"
        urlxp = link + "/index.txt"
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        a1 = InlineKeyboardButton(text=f"تشغيل قائمة تشغيل المجموعة", callback_data=f'play_playlist {user_id}|group')
        a3 = InlineKeyboardButton(text=f"📨 تحقق من قائمة التشغيل", url=urlxp)
        key = InlineKeyboardMarkup(
            [
                [
                    a1,
                ],
                [
                    a3,
                    InlineKeyboardButton(text="🗑 إغلاق القائمة", callback_data=f'close2')
                ]    
            ]
        )
        if await isPreviewUp(preview):
            try:
                await CallbackQuery.message.reply_photo(
                    photo=preview, quote=False, reply_markup=key
                )
                await m.delete()
            except Exception:
                pass
        else:
            await CallbackQuery.message.reply_photo(
                    photo=link, quote=False, reply_markup=key
                )
            await m.delete()
                       
        
@Client.on_callback_query(filters.regex("cbgroupdel"))
async def cbgroupdel(_,CallbackQuery):  
    a = await app.get_chat_member(CallbackQuery.message.chat.id , CallbackQuery.from_user.id)
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer("ليس لديك إذن مطلوب لأداء هذا الإجراء.\nPermission: MANAGE VOICE CHATS", show_alert=True)
    await CallbackQuery.message.delete() 
    await CallbackQuery.answer()
    _playlist = await get_note_names(CallbackQuery.message.chat.id)                                    
    if not _playlist:
        return await CallbackQuery.message.reply_text("Group has no Playlist on Music's Server")
    else:
        titlex = []
        for note in _playlist:
            await delete_playlist(CallbackQuery.message.chat.id, note)
    await CallbackQuery.message.reply_text("Successfully deleted your Group's whole playlist")  
    
    
@Client.on_callback_query(filters.regex("cbdel"))
async def delplcb(_,CallbackQuery): 
    await CallbackQuery.answer()
    await CallbackQuery.message.delete() 
    _playlist = await get_note_names(CallbackQuery.from_user.id)                                    
    if not _playlist:
        return await CallbackQuery.message.reply_text("You have no Playlist on Music's Server")
    else:
        titlex = []
        for note in _playlist:
            await delete_playlist(CallbackQuery.from_user.id, note)
    await CallbackQuery.message.reply_text("Successfully deleted your whole playlist")


@Client.on_callback_query(filters.regex("nglish"))
async def nglish(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""
**[🗣]({BOT_IMG}) مرحبا هل انت مستعد لاستخدامي?

🔖  يمكنك استخدامي للاستماع إلى الأغاني في الدردشة الصوتية ويمكن تشغيل مقاطع الفيديو في الدردشة الصوتية!

📑 To Find Out All The Available Command Bots, You Can Press The Two Buttons Below, Namely Cmd Music And Cmd Stream**

""",
        reply_markup=InlineKeyboardMarkup(
        [
        [
            InlineKeyboardButton(
                "⚔️Add Me To Your Group⚔️", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
        ],
        [
           InlineKeyboardButton("👁️︙owner︙👁️", callback_data="jwner"),
        ],
        [
            InlineKeyboardButton("🔭︙support group", url=f"https://t.me/{GROUP}"),
            InlineKeyboardButton("📡︙Source channel", url=f"https://t.me/{CHANNEL}"),
        ],
        [
            InlineKeyboardButton("🎟︙commands", url="https://telegra.ph/Xzero-01-19"),
        ],
        [
           InlineKeyboardButton("🏴‍☠️︙programmer", callback_data="sthjbt"),
        ],
        [
           InlineKeyboardButton("🔙︙back", callback_data="xback"),
        ],
        ]
   ),
 )

@Client.on_callback_query(filters.regex("rabic"))
async def rabic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""
**[🗣]({BOT_IMG}) مرحبا بك! جاهز استخدمني?

🔖 انا بوت يمكن استخدامه للاستماع إلى الأغاني في الدردشة الصوتية ويمكن تشغيل مقاطع الفيديو في الدردشة الصوتية!

📑 ولمعرفة جميع اوامر البوت المتاحة، يمكنك الضغط على زر الاوامر ادناه**

""",
        reply_markup=InlineKeyboardMarkup(
        [
        [
            InlineKeyboardButton(
                "⚔️اضاف البوت الى مجموعتك⚔️", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
        ],
        [
           InlineKeyboardButton("👁️︙المالك︙👁️", callback_data="esany"),
        ],
        [
            InlineKeyboardButton("🔭︙جروب الدعم", url=f"https://t.me/{GROUP}"),
            InlineKeyboardButton("📡︙قناه السورس", url=f"https://t.me/{CHANNEL}"),
        ],
        [
            InlineKeyboardButton("🎟︙الاوامر", url="https://telegra.ph/XERO-01-19"),
        ],
        [
           InlineKeyboardButton("🏴‍☠️︙المبرمج", callback_data="vhkcbt"),
        ],
        [
           InlineKeyboardButton("🔙︙رجــــــوع", callback_data="xback"),
        ],
        ]
   ),
 )
 
@Client.on_callback_query(filters.regex("turkish"))
async def turkish(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""
**[🗣]({BOT_IMG}) Merhaba! Beni Kullanmaya Hazır mısın?

🔖  Sesli Sohbette Şarkı Dinlemek İçin Kullanılabilen Ve Sesli Sohbette Video Oynatabilen Bir Bot!

📑 Mevcut Tüm Komut Botlarını Bulmak İçin Aşağıdaki İki Düğmeye Basabilirsiniz, yani Cmd Müzik ve Cmd Akışı**

""",
        reply_markup=InlineKeyboardMarkup(
        [
        [
            InlineKeyboardButton(
                "⚔️Beni Grubuna Ekle⚔️", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
        ],
        [
           InlineKeyboardButton("👁️︙sahip︙👁️", callback_data="ahibinin"),
        ],
        [
            InlineKeyboardButton("🔭︙destek grubu", url=f"https://t.me/{GROUP}"),
            InlineKeyboardButton("📡︙kaynak kanalı", url=f"https://t.me/{CHANNEL}"),
        ],
        [
            InlineKeyboardButton("🎟︙komutlar", url="https://telegra.ph/XERO-03-24-2"),
        ],
        [
           InlineKeyboardButton("🏴‍☠️︙programcı", callback_data="kopset"),
        ],
        [
           InlineKeyboardButton("🔙︙geri", callback_data="xback"),
        ],
        ]
   ),
 )

@Client.on_callback_query(filters.regex("persian"))
async def persian(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""
**[🗣]({BOT_IMG}) سلام! آماده استفاده از من؟

🔖  روباتی است که می توان از آن برای گوش دادن به آهنگ ها در چت صوتی و پخش ویدیوها در چت صوتی استفاده کرد!

📑 برای پیدا کردن تمام دستورات ربات موجود، می توانید دکمه فرمان زیر را فشار دهید**

""",
        reply_markup=InlineKeyboardMarkup(
        [
        [
            InlineKeyboardButton(
                "⚔️من را به گروه خود اضافه کنید⚔️", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
        ],
        [
           InlineKeyboardButton("👁️︙مالک︙👁️", callback_data="ipooy"),
        ],
        [
            InlineKeyboardButton("🔭︙گروه پشتیبانی", url=f"https://t.me/{GROUP}"),
            InlineKeyboardButton("📡︙کانال منبع", url=f"https://t.me/{CHANNEL}"),
        ],
        [
            InlineKeyboardButton("🎟︙دستورات", url="https://telegra.ph/XERo-03-24"),
        ],
        [
           InlineKeyboardButton("🏴‍☠️︙برنامه نویس", callback_data="elkeatib"),
        ],
        [
           InlineKeyboardButton("🔙︙بازگشت", callback_data="xback"),
        ],
        ]
   ),
 )

@Client.on_callback_query(filters.regex("vhkcbt"))
async def vhkcbt(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""[👌]({OT_IMG}) هلا ومرحبا بك هنا يمكن لك التواصل مع المبرمج ومن هنا يمكن لك استخراج اشياء التنصيب""",
        reply_markup=InlineKeyboardMarkup(
            [
                [        
                    InlineKeyboardButton(
                        "𝚃𝙸𝚃𝙾", url=f"https://t.me/XXX_xx_XXX0"
                    ),
                ],
                [                    
                    InlineKeyboardButton(
                        "🌍 ¦ لو عيز تنصب ", callback_data="vzerfg" 
                    ),        
                ],
                [                  
                    InlineKeyboardButton(
                        "🔙 ︙رجــــــوع", callback_data="rabic" 
                    ),  
                ],
            ]
        ),
    )         
    
    
@Client.on_callback_query(filters.regex("xback"))
async def xback(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""
**[🗣]({BOT_IMG}) مرحبا ! جاهز لى استخدامي?

🔖 انا روبوت يمكن استخدامه للاستماع إلى الأغاني في الدردشة الصوتية ويمكنه تشغيل مقاطع الفيديو في الدردشة الصوتية!

🤖 ويمكن لك تحديد اللغة من الازرار في الاسفل**

**🗣 Hello ! Ready Use Me?

🔖 يمكنك استخدامي للاستماع إلى الأغاني في الدردشة الصوتية ويمكن تشغيل مقاطع الفيديو في الدردشة الصوتية!

🤖 ويمكنك تحديد اللغة من الأزرار بلاسفل**

""",
        reply_markup=InlineKeyboardMarkup(
        [
        [
            InlineKeyboardButton("🏴‍☠️︙اللغه العربية", callback_data="rabic"),
        ],
        [
            InlineKeyboardButton("🇬🇧︙English language", callback_data="nglish"),
        ],
        [
           InlineKeyboardButton("🇹🇷︙Turkish", callback_data="turkish"),
           InlineKeyboardButton("🇮🇷︙Persian", callback_data="persian"),
        ],
        ]
   ),
 )
 
 
@Client.on_callback_query(filters.regex("sthjbt"))
async def sthjbt(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""[👌]({OT_IMG}) Hala and welcome here you can communicate with the programmer and from here you can extract the things of the inauguration""",
        reply_markup=InlineKeyboardMarkup(
            [
                [        
                    InlineKeyboardButton(
                        "𝚃𝙸𝚃𝙾", url=f"https://t.me/XXX_xx_XXX0"
                    ),
                ],
                [                    
                    InlineKeyboardButton(
                        "💻︙Install", callback_data="hasht"
                    ),        
                ],
                [                  
                    InlineKeyboardButton(
                        "🔙︙back", callback_data="nglish" 
                    ),  
                ],
            ]
        ),
    )         
    
    
@Client.on_callback_query(filters.regex("kopset"))
async def kopset(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""[👌]({OT_IMG}) Hala ve hoşgeldiniz buradan programcı ile iletişime geçebilir ve buradan açılışla ilgili şeyleri çıkarabilirsiniz.""",
        reply_markup=InlineKeyboardMarkup(
            [
                [        
                    InlineKeyboardButton(
                        "𝚃𝙸𝚃𝙾", url=f"https://t.me/XXX_xx_XXX0"
                    ),
                ],
                [                    
                    InlineKeyboardButton(
                        "💻︙Düzenlemek", callback_data="tshels"
                    ),        
                ],
                [                  
                    InlineKeyboardButton(
                        "🔙︙geri", callback_data="turkish" 
                    ),  
                ],
            ]
        ),
    )         
    
    
@Client.on_callback_query(filters.regex("elkeatib"))
async def elkeatib(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""[👌]({OT_IMG}) سلام و خوش آمدید اینجا می توانید با برنامه نویس ارتباط برقرار کنید و از اینجا می توانید موارد افتتاحیه را استخراج کنید.""",
        reply_markup=InlineKeyboardMarkup(
            [
                [        
                    InlineKeyboardButton(
                        "𝚃𝙸𝚃𝙾", url=f"https://t.me/XXX_xx_XXX0"
                    ),
                ],
                [                    
                    InlineKeyboardButton(
                        "💻︙نصب", callback_data="hossam"
                    ),        
                ],
                [                  
                    InlineKeyboardButton(
                        "🔙︙بازگشت", callback_data="persian" 
                    ),  
                ],
            ]
        ),
    )         
    
    
@Client.on_callback_query(filters.regex("hasht"))
async def hasht(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""[👌]({OT_IMG}) Connect with the developers me a song bot is installed for you""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                   InlineKeyboardButton("𓄼⦁ 𝗝ٰٖ𝗔ٰٖ𝗕ٰٖ𝗪ٰٖ𝗔ٰٖ ➪🇳🇱⦁𓄹", url=f"https://t.me/JABWA"),
                   InlineKeyboardButton("･ 𓆩ᎫᎬᏦᎪ 𖤐", url=f"https://t.me/Dev_Jeka"),
                ],
                [                  
                    InlineKeyboardButton(
                        "🔙︙back", callback_data="sthjbt"),  
                ],
            ]
        ),
    )         
    
    
@Client.on_callback_query(filters.regex("vzerfg"))
async def vzerfg(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""[👌]({OT_IMG}) قم التواصل مع المطورين لي يتم تنصيب بوت اغاني لك""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                   InlineKeyboardButton("𓄼⦁ 𝗝ٰٖ𝗔ٰٖ𝗕ٰٖ𝗪ٰٖ𝗔ٰٖ ➪🇳🇱⦁𓄹", url=f"https://t.me/JABWA"),
                   InlineKeyboardButton("･ 𓆩ᎫᎬᏦᎪ 𖤐", url=f"https://t.me/Dev_Jeka"),
                ],
                [                  
                    InlineKeyboardButton(
                        "🔙 ︙رجــــــوع", callback_data="vhkcbt"),  
                ],
            ]
        ),
    )         
    
    
@Client.on_callback_query(filters.regex("tshels"))
async def tshels(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""[👌]({OT_IMG}) Geliştiricilerle bağlantı kurun, sizin için bir şarkı botu yüklendi""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                   InlineKeyboardButton("𓄼⦁ 𝗝ٰٖ𝗔ٰٖ𝗕ٰٖ𝗪ٰٖ𝗔ٰٖ ➪🇳🇱⦁𓄹", url=f"https://t.me/JABWA"),
                   InlineKeyboardButton("･ 𓆩ᎫᎬᏦᎪ 𖤐", url=f"https://t.me/Dev_Jeka"),
                ],
                [                  
                    InlineKeyboardButton(
                        "🔙︙geri", callback_data="kopset"),  
                ],
            ]
        ),
    )         
    
    
@Client.on_callback_query(filters.regex("hossam"))
async def hossam(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""[👌]({OT_IMG}) با توسعه دهندگان به من یک موتور آهنگ برای شما نصب شده است""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                   InlineKeyboardButton("𓄼⦁ 𝗝ٰٖ𝗔ٰٖ𝗕ٰٖ𝗪ٰٖ𝗔ٰٖ ➪🇳🇱⦁𓄹", url=f"https://t.me/JABWA"),
                   InlineKeyboardButton("･ 𓆩ᎫᎬᏦᎪ 𖤐", url=f"https://t.me/Dev_Jeka"),
                ],
                [                  
                    InlineKeyboardButton(
                        "🔙︙بازگشت", callback_data="elkeatib"),  
                ],
            ]
        ),
    )         
    
    
@Client.on_callback_query(filters.regex("esany"))
async def esany(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""[🙂]({MOT_IMG}) هلا ومرحبا بك هنا يمكن لك التواصل مع صاحب البوت""",
        reply_markup=InlineKeyboardMarkup(
            [
                [        
                    InlineKeyboardButton(
                        "صاحب البوت", url=f"https://t.me/{OWNER_USERNAME}"),
                ],
                [
                    InlineKeyboardButton("🔭︙جروب المالك", url=f"https://t.me/{ROUP}"),
                    InlineKeyboardButton("📡︙قناه المالك", url=f"https://t.me/{HANNEL}"),
                ],
                [                  
                    InlineKeyboardButton(
                        "🔙 ︙رجــــــوع", callback_data="rabic" 
                    ),  
                ],
            ]
        ),
    )         
    
    
@Client.on_callback_query(filters.regex("jwner"))
async def jwner(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""[🙂]({MOT_IMG}) Hello and welcome here. You can contact the owner of the bot""",
        reply_markup=InlineKeyboardMarkup(
            [
                [        
                    InlineKeyboardButton(
                        "bot owner", url=f"https://t.me/{OWNER_USERNAME}"),
                ],
                [
                    InlineKeyboardButton("🔭︙Owner's group", url=f"https://t.me/{ROUP}"),
                    InlineKeyboardButton("📡︙Owner's channel", url=f"https://t.me/{HANNEL}"),
                ],
                [                  
                    InlineKeyboardButton(
                        "🔙︙back", callback_data="nglish" 
                    ),  
                ],
            ]
        ),
    )         
    
    
@Client.on_callback_query(filters.regex("ipooy"))
async def ipooy(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""[🙂]({MOT_IMG}) سلام و خوش آمدید. می توانید با صاحب ربات تماس بگیرید""",
        reply_markup=InlineKeyboardMarkup(
            [
                [        
                    InlineKeyboardButton(
                        "صاحب ربات", url=f"https://t.me/{OWNER_USERNAME}"),
                ],
                [
                    InlineKeyboardButton("🔭︙گروه مالک", url=f"https://t.me/{ROUP}"),
                    InlineKeyboardButton("📡︙کانال مالک", url=f"https://t.me/{HANNEL}"),
                ],
                [                  
                    InlineKeyboardButton(
                        "🔙︙بازگشت", callback_data="nglish" 
                    ),  
                ],
            ]
        ),
    )         
    
    
@Client.on_callback_query(filters.regex("ahibinin"))
async def ahibinin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""[🙂]({MOT_IMG}) Merhaba ve buraya hoş geldiniz. Botun sahibiyle iletişime geçebilirsiniz""",
        reply_markup=InlineKeyboardMarkup(
            [
                [        
                    InlineKeyboardButton(
                        "bot sahibi", url=f"https://t.me/{OWNER_USERNAME}"),
                ],
                [
                    InlineKeyboardButton("🔭︙Sahibinin grubu", url=f"https://t.me/{ROUP}"),
                    InlineKeyboardButton("📡︙Sahibin kanalı", url=f"https://t.me/{HANNEL}"),
                ],
                [                  
                    InlineKeyboardButton(
                        "🔙︙geri", callback_data="turkish" 
                    ),  
                ],
            ]
        ),
    )         
    
    