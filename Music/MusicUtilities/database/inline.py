from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
from Music.config import GROUP, CHANNEL


def play_markup(videoid, user_id):
    buttons= [
            [
                InlineKeyboardButton(text="🔭︙جروب الدعم", url=f"https://t.me/{GROUP}"),
            ],
            [      
                InlineKeyboardButton(text="🎰︙القائمه", callback_data=f'other {videoid}|{user_id}'),
                InlineKeyboardButton(text="🗑️ اغلاق", callback_data=f'close2')
            ],
        ]
    return buttons 


def others_markup(videoid, user_id):
    buttons= [
            [
                InlineKeyboardButton(text="▶️", callback_data=f'resumevc'),
                InlineKeyboardButton(text="⏸️", callback_data=f'pausevc'),
                InlineKeyboardButton(text="⏭️", callback_data=f'skipvc'),
                InlineKeyboardButton(text="⏹️", callback_data=f'stopvc'),
            ],
            [
                InlineKeyboardButton(text="🎸 Add Your List", callback_data=f'playlist {videoid}|{user_id}'),
                InlineKeyboardButton(text="🎸 Add Group List", callback_data=f'group_playlist {videoid}|{user_id}')
            ],
            [
                InlineKeyboardButton(text="📮 Get Audio", callback_data=f'gets audio|{videoid}|{user_id}'),
                InlineKeyboardButton(text="📮 Get Video", callback_data=f'gets video|{videoid}|{user_id}')
            ],
            [
                InlineKeyboardButton(text="⏪ Back To Button", callback_data=f'goback {videoid}|{user_id}'),
            ],
        ]
    return buttons 




play_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "▶️", callback_data="resumevc"
                    ),
                    InlineKeyboardButton(
                        "⏸️", callback_data="pausevc"
                    ),
                    InlineKeyboardButton(
                        "⏭️", callback_data="skipvc"
                    ),
                    InlineKeyboardButton(
                        "⏹️", callback_data="stopvc"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🎰︙إغلاق القائمة", callback_data="close"
                    )
                ]    
            ]
        )



def audio_markup(videoid, user_id):
    buttons= [
            [
                InlineKeyboardButton(text="▶️", callback_data=f'resumevc'),
                InlineKeyboardButton(text="⏸️", callback_data=f'pausevc'),
                InlineKeyboardButton(text="⏭️", callback_data=f'skipvc'),
                InlineKeyboardButton(text="⏹️", callback_data=f'stopvc')
            ],
            [
                InlineKeyboardButton(text="🎰︙إغلاق القائمة", callback_data="close2")              
            ],
        ]
    return buttons 


def search_markup(ID1, ID2, ID3, ID4, ID5, duration1, duration2, duration3, duration4, duration5, user_id, query):
    buttons= [
            [
                InlineKeyboardButton(text="1️⃣", callback_data=f'Music2 {ID1}|{duration1}|{user_id}'),
                InlineKeyboardButton(text="2️⃣", callback_data=f'Music2 {ID2}|{duration2}|{user_id}'),
                InlineKeyboardButton(text="3️⃣", callback_data=f'Music2 {ID3}|{duration3}|{user_id}')
            ],
            [ 
                InlineKeyboardButton(text="4️⃣", callback_data=f'Music2 {ID4}|{duration4}|{user_id}'),
                InlineKeyboardButton(text="5️⃣", callback_data=f'Music2 {ID5}|{duration5}|{user_id}')
            ],
            [ 
                
                InlineKeyboardButton(text="⬅️", callback_data=f'popat 1|{query}|{user_id}'), 
                InlineKeyboardButton(text="❌​", callback_data=f"ppcl2 smex|{user_id}") ,
                InlineKeyboardButton(text="➡️", callback_data=f'popat 1|{query}|{user_id}')             
            ],
        ]
    return buttons   

def search_markup2(ID6, ID7, ID8, ID9, ID10, duration6, duration7, duration8, duration9, duration10 ,user_id, query):
    buttons= [
            [
                InlineKeyboardButton(text="6️⃣", callback_data=f'Music2 {ID6}|{duration6}|{user_id}'),
                InlineKeyboardButton(text="7️⃣", callback_data=f'Music2 {ID7}|{duration7}|{user_id}'),
                InlineKeyboardButton(text="8️⃣", callback_data=f'Music2 {ID8}|{duration8}|{user_id}')
            ],
            [ 
                InlineKeyboardButton(text="9️⃣", callback_data=f'Music2 {ID9}|{duration9}|{user_id}'),
                InlineKeyboardButton(text="🔟", callback_data=f'Music2 {ID10}|{duration10}|{user_id}')
            ],
            [ 
                
                InlineKeyboardButton(text="⬅️", callback_data=f'popat 2|{query}|{user_id}'), 
                InlineKeyboardButton(text="❌", callback_data=f"ppcl2 smex|{user_id}") ,
                InlineKeyboardButton(text="➡️", callback_data=f'popat 2|{query}|{user_id}')             
            ],
        ]
    return buttons 


def personal_markup(link):
    buttons= [
            [
                InlineKeyboardButton(text="Watch On Youtube", url=f'{link}')
            ],
            [ 
                InlineKeyboardButton(text="🗑️ اغلاق", callback_data=f'close2')
            ],
        ]
    return buttons   
  
start_keyboard = InlineKeyboardMarkup( 
            [
                [
                    InlineKeyboardButton(
                        "🎟︙الاوامر", url="https://telegra.ph/XERO-01-19"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🎰︙إغلاق القائمة", callback_data="close2"
                    )
                ]    
            ]
        )
    
confirm_keyboard = InlineKeyboardMarkup( 
            [
                [
                    InlineKeyboardButton(
                        "Yes", callback_data="cbdel"
                    ),
                    InlineKeyboardButton(
                        "No", callback_data="close2"
                    )
                ]    
            ]
        )

confirm_group_keyboard = InlineKeyboardMarkup( 
            [
                [
                    InlineKeyboardButton(
                        "Yes", callback_data="cbgroupdel"
                    ),
                    InlineKeyboardButton(
                        "No", callback_data="close2"
                    )
                ]    
            ]
        )

close_keyboard = InlineKeyboardMarkup( 
            [
                [
                    InlineKeyboardButton(
                        "🗑️ اغلاق", callback_data="close2"
                    )
                ]    
            ]
        )

play_list_keyboard = InlineKeyboardMarkup( 
            [
                [
                    InlineKeyboardButton(
                        "Users Playlist", callback_data="P_list"
                    ),
                    InlineKeyboardButton(
                        "Groups Playlist", callback_data="G_list"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑️ اغلاق", callback_data="close2"
                    )
                ]
            ]
        )

def playlist_markup(user_name, user_id):
    buttons= [
            [
                InlineKeyboardButton(text=f"Groups", callback_data=f'play_playlist {user_id}|group'),
                InlineKeyboardButton(text=f"{user_name[:8]}", callback_data=f'play_playlist {user_id}|personal'),
            ],
            [
                InlineKeyboardButton(text="🗑 Close Playlist", callback_data="close2")              
            ],
        ]
    return buttons
