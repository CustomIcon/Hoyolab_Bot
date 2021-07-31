from bot import bot, loop
from bot.db import Database
from pyrogram import types
import genshinstats as gs


DEFAULT_BUTTONS = {
    1: [[types.InlineKeyboardButton('Your Characters', switch_inline_query_current_chat='characters ')]],
    2: [[types.InlineKeyboardButton('Your Exploration', switch_inline_query_current_chat='exploration ')]],

}

DEFAULT_HELP = {
    1: '✨ List out all characters owned with details ~',
    2: '✨ View your Current Exploration Progress ~',
}

DEFAULT_THUMB = {
    1: 'https://static.wikia.nocookie.net/gensin-impact/images/a/ab/Character_Noelle_Thumb.png/revision/latest/smart/width/250/height/250?cb=20210214011929',
    2: 'https://static.wikia.nocookie.net/gensin-impact/images/8/80/Emblem_Mondstadt.png/revision/latest?cb=20201116194623',
}

DEFAULT_TITLE = {
    1: 'Characters Owned',
    2: 'Exploration Progress',
}



@bot.on_inline_query()
async def inline_handle(_, query: types.InlineQuery):
    db = Database()
    string = query.query.lower()
    answers = []
    user = db.find_by_user_id(query.from_user.id)
    if not user:
        await query.answer(
            results=answers,
            switch_pm_text=f'You are not logged in, PM me to login to hoyolab',
            switch_pm_parameter='register',
            cache_time=0,
        )
        return
    if string == '':
        try:
            text = "╒═══「  **Stats**  」\n"
            for key, value in (
                await loop.run_in_executor(
                    None,
                    lambda: gs.get_user_stats(
                        int(user)
                    )
                )
            )['stats'].items():
                text += f"│ • {key.replace('_', ' ')}: `{value}`\n"
            text += f"╘══「 **UID**: `{user}`  」\n"
            answers.append(
                types.InlineQueryResultArticle(
                    title='Your Current IG Stats',
                    description='✨ View your Current In-game stats ~',
                    input_message_content=types.InputTextMessageContent(
                        text,
                        parse_mode='markdown',
                        disable_web_page_preview=True,
                    ),
                    thumb_url='https://ih1.redbubble.net/image.1938712092.4010/st,small,507x507-pad,600x600,f8f8f8.jpg',
                ),
            )
        except gs.errors.DataNotPublic:
            text = "Logged Out"
            answers.append(
                types.InlineQueryResultArticle(
                    title='Your Data is not public Anymore, Bot will automatically log you out',
                    description='Sorry-Masen',
                    input_message_content=types.InputTextMessageContent(
                        text,
                        parse_mode='markdown',
                        disable_web_page_preview=True,
                    ),
                    thumb_url='https://imgr.search.brave.com/vNgyG_vik5zyeHdev1X6J4KvF0BLg0SJ4iW425jy7sI/fit/600/600/no/1/aHR0cHM6Ly9pLnBp/bmltZy5jb20vNzM2/eC82Yy9lNi9hNi82/Y2U2YTZmYWIzNzUy/NzE4ZTIyZGEzMGZi/MjE0Y2FhYS5qcGc',
                ),
            )
            return await bot.answer_inline_query(
                query.id,
                results=answers,
                is_gallery=False,
                cache_time=0,
            )
        for i in range(1, 3):
            answers.append(
                types.InlineQueryResultArticle(
                    title=DEFAULT_TITLE[i],
                    description=DEFAULT_HELP[i],
                    input_message_content=types.InputTextMessageContent(
                        DEFAULT_HELP[i],
                        parse_mode='markdown',
                        disable_web_page_preview=True,
                    ),
                    reply_markup=types.InlineKeyboardMarkup(DEFAULT_BUTTONS[i]),
                    thumb_url=DEFAULT_THUMB[i],
                ),
            )
    # 🌪 ⛰ 🔥 ⚡️ 🍃 ❄️
    elif string.split()[0] == 'characters':
        for character in await loop.run_in_executor(None, lambda: gs.get_characters(int(user))):
            if character['element'].lower() == 'hydro':
                element = '💧'
            elif character['element'].lower() == 'cryo':
                element = '❄️'
            elif character['element'].lower() == 'electro':
                element = '⚡️'
            elif character['element'].lower() == 'anemo':
                element = '🌪'
            elif character['element'].lower() == 'dendro':
                element = '🌱'
            elif character['element'].lower() == 'pyro':
                element = '🔥'
            elif character['element'].lower() == 'geo':
                element = '⛰'
            name = f"Traveler({character['element']})" if character['name'] == "Traveler" else character['name']
            text = f"{element} **{character['name']}** {''.join('⭐️' for _ in range(character['rarity']))}\n"
            text += "=============\n"
            text += f"**Level**: {character['level']}\n"
            text += f"**Friendship**: {character['friendship']}\n"
            text += f"**Constellation**: {character['constellation']}\n"
            if len(character['outfits']) != 0:
                text += f"**Outfit**:\n"
                for outfit in character['outfits']:
                    text += f"- {outfit['name']}\n"
            answers.append(
                types.InlineQueryResultArticle(
                    title=name,
                    description=f"{character['element']} | level {character['level']}",
                    input_message_content=types.InputTextMessageContent(
                        text,
                        parse_mode='markdown',
                    ),
                    thumb_url=character["icon"].replace('_image', '_icon').replace('@2x', ''),
                    reply_markup=types.InlineKeyboardMarkup(
                        [
                            [
                                types.InlineKeyboardButton(
                                    'Weapon', callback_data=f'w_{character["name"]}_{query.from_user.id}'
                                ),
                                types.InlineKeyboardButton(
                                    'Artifacts', callback_data=f'a_{character["name"]}_{query.from_user.id}'
                                )
                            ],
                            [
                                types.InlineKeyboardButton(
                                    'Constellation', callback_data=f'c_{character["name"]}_{query.from_user.id}'
                                ),
                                types.InlineKeyboardButton(
                                    'Characters', switch_inline_query_current_chat=f'characters '
                                )
                            ]
                    
                        ]
                    )
                )
            )
    elif string.split()[0] == 'exploration':
        for exp in gs.get_user_stats(int(user))['explorations']:
            name = exp['name']
            explored = exp['explored']
            type = exp['type']
            level = exp['level']
            text = f"**Name**: `{name}`\n"
            text += f"**Type**: `{type}`\n"
            text += f"**Level**: `{level}`\n"
            text += f"**Explored**: `{explored}`\n"
            answers.append(
                types.InlineQueryResultArticle(
                    title=name,
                    description=f"Level: {level}",
                    input_message_content=types.InputTextMessageContent(
                        text,
                        parse_mode='markdown',
                    ),
                    thumb_url=exp['icon']
                )
            )
            
    await bot.answer_inline_query(
        query.id,
        results=answers,
        is_gallery=False,
        cache_time=0,
    )