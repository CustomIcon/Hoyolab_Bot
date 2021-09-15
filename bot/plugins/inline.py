from bot import bot, loop
from bot.db import Database
from pyrogram import types
import genshinstats as gs
from genshinstats.utils import recognize_server


DEFAULT_BUTTONS = {
    1: [[types.InlineKeyboardButton('Your Characters', switch_inline_query_current_chat='characters ')]],
    2: [[types.InlineKeyboardButton('Your Exploration', switch_inline_query_current_chat='exploration ')]],
    3: [[types.InlineKeyboardButton('Your Teapots', switch_inline_query_current_chat='teapots ')]],
}

DEFAULT_HELP = {
    1: '✨ List out all characters owned with details ~',
    2: '✨ View your Current Exploration Progress ~',
    3: '✨ View your Teapot Progress ~',
    4: '✨ Spiral Abyss Stats ~',
}

DEFAULT_THUMB = {
    1: 'https://static.wikia.nocookie.net/gensin-impact/images/a/ab/Character_Noelle_Thumb.png/revision/latest/smart/width/250/height/250?cb=20210214011929',
    2: 'https://static.wikia.nocookie.net/gensin-impact/images/8/80/Emblem_Mondstadt.png/revision/latest?cb=20201116194623',
    3: 'https://static.wikia.nocookie.net/gensin-impact/images/5/5a/Item_Serenitea_Pot.png',
    4: 'https://gblobscdn.gitbook.com/spaces%2F-MVAGyyACcSzyzfmgy7f%2Favatar-1615191145426.png?alt=media'
}

DEFAULT_TITLE = {
    1: 'Characters Owned',
    2: 'Exploration Progress',
    3: 'Teapot Progress',
    4: 'Spiral Abyss stats'
}


@bot.on_inline_query(group=5)
async def inline_handle(_, query: types.InlineQuery):
    answers = []
    if not Database().find_by_user_id(query.from_user.id):
        await query.answer(
            results=answers,
            switch_pm_text=f'You are not logged in, PM me to login to hoyolab',
            switch_pm_parameter='register',
            cache_time=0,
        )
        return
    try:
        text = '╒═══「  **Stats**  」\n'
        for key, value in (
            await loop.run_in_executor(
                None,
                lambda: gs.get_user_stats(
                    int(Database().find_by_user_id(query.from_user.id)),
                ),
            )
        )['stats'].items():
            text += f"│ • {key.replace('_', ' ')}: `{value}`\n"
        text += f'│ • server: `{await loop.run_in_executor(None, lambda: recognize_server(int(Database().find_by_user_id(query.from_user.id))))}`\n'
        text += f'╘══「 **UID**: `{Database().find_by_user_id(query.from_user.id)}`  」\n'
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
        text = 'Logged Out'
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
    for i in range(1, 5):
        answers.append(
            types.InlineQueryResultArticle(
                title=DEFAULT_TITLE[i],
                description=DEFAULT_HELP[i],
                input_message_content=types.InputTextMessageContent(
                    DEFAULT_HELP[i],
                    parse_mode='markdown',
                    disable_web_page_preview=True,
                ),
                reply_markup=types.InlineKeyboardMarkup(
                    DEFAULT_BUTTONS[i],
                ),
                thumb_url=DEFAULT_THUMB[i],
            ),
        )
    await bot.answer_inline_query(
        query.id,
        results=answers,
        is_gallery=False,
        cache_time=0,
    )
