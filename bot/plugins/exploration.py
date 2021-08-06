from bot import bot, loop
from bot.db import Database
from pyrogram import types, filters
import genshinstats as gs

@bot.on_inline_query(filters.regex('exploration'))
async def explorations(_, query: types.InlineQuery):
    answers = []
    for exp in (
        await loop.run_in_executor(
            None,
            lambda: gs.get_user_stats(
                int(Database().find_by_user_id(query.from_user.id))
            )
        )
    )['explorations']:
        name = exp['name']
        explored = exp['explored']
        type = exp['type']
        level = exp['level']
        text = f'**Name**: `{name}`\n'
        text += f'**Type**: `{type}`\n'
        text += f'**Level**: `{level}`\n'
        text += f'**Explored**: `{explored}`\n'
        answers.append(
            types.InlineQueryResultArticle(
                title=name,
                description=f'Level: {level}',
                input_message_content=types.InputTextMessageContent(
                    text,
                    parse_mode='markdown',
                ),
                thumb_url=exp['icon'],
            ),
        )
    await bot.answer_inline_query(
        query.id,
        results=answers,
        is_gallery=False,
        cache_time=0,
    )