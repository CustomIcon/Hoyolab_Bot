from bot import bot, loop
from bot.db import Database
from pyrogram import types, filters
import genshinstats as gs

@bot.on_inline_query(filters.regex('teapots'))
async def teapots(_, query: types.InlineQuery):
    answers = []
    for teapot in (
        await loop.run_in_executor(
            None,
            lambda: gs.get_user_stats(int(Database().find_by_user_id(query.from_user.id)))
        )
    )['teapots']:
        text = f'**Name**: `{teapot["name"]}`\n'
        text += f'**Level**: `{teapot["level"]}`\n'
        text += f'**Total Items**: `{teapot["placed_items"]}`\n'
        text += f'**Visitors (Real-Time)**: `{teapot["visitors"]}`\n'
        text += f'**Total Adeptus Energy**: `{teapot["comfort"]}`\n'
        answers.append(
            types.InlineQueryResultArticle(
                title=teapot["name"],
                input_message_content=types.InputTextMessageContent(
                    text,
                    parse_mode='markdown',
                ),
                thumb_url='https://static.wikia.nocookie.net/gensin-impact/images/5/56/Emblem_Serenitea_Pot.png',
            ),
        )
    await bot.answer_inline_query(
        query.id,
        results=answers,
        is_gallery=False,
        cache_time=0,
    )