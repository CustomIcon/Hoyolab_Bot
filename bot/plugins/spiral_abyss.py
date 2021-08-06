from gc import callbacks
from bot import bot, loop
from bot.db import Database
from pyrogram import types, filters
import genshinstats as gs

@bot.on_inline_query(filters.regex('spiral'))
async def spiral_abyss(_, query: types.InlineQuery):
    answers = []
    res = await loop.run_in_executor(None, lambda: gs.get_spiral_abyss(int(Database().find_by_user_id(query.from_user.id))))
    text = f"**Spiral Abyss Season: {res['season']} from** `{res['season_start_time']}` **to** `{res['season_end_time']}`:\n"
    text += f"Total Battles: {res['stats']['total_battles']}\n"
    text += f"Total Wins: {res['stats']['total_wins']}\n"
    text += f"Max Floor: {res['stats']['max_floor']}\n"
    text += f"Total Stars: {res['stats']['total_stars']}\n\n"
    text += f"Most Played Character: {res['character_ranks']['most_played'][0]['name']} - {res['character_ranks']['most_played'][0]['value']} times\n"
    text += f'Most kills: {res["character_ranks"]["most_kills"][0]["name"]} - {res["character_ranks"]["most_kills"][0]["value"]} kills\n'
    text += f'Strongest Strike: {res["character_ranks"]["strongest_strike"][0]["name"]} - {res["character_ranks"]["strongest_strike"][0]["value"]} DMG\n'
    text += f'Most DMG Taken: {res["character_ranks"]["most_damage_taken"][0]["name"]} - {res["character_ranks"]["most_damage_taken"][0]["value"]} dmg taken\n'
    text += f'Most Bursts Used: {res["character_ranks"]["most_bursts_used"][0]["name"]} - {res["character_ranks"]["most_bursts_used"][0]["value"]} bursts\n'
    text += f'Most Skills Used: {res["character_ranks"]["most_skills_used"][0]["name"]} - {res["character_ranks"]["most_skills_used"][0]["value"]} times\n'
    answers.append(
        types.InlineQueryResultArticle(
            title="Spiral Abyss Data",
            description=f"Max Floor: {res['stats']['max_floor']}",
            input_message_content=types.InputTextMessageContent(
                text,
                parse_mode='markdown',
            ),
            reply_markup=types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton("Floor Details", callback_data=f"floor_{query.from_user.id}")
                    ]
                ]
            )
        ),
    )
    await bot.answer_inline_query(
        query.id,
        results=answers,
        is_gallery=False,
        cache_time=0,
    )