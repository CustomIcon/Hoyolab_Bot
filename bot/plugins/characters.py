from bot import bot, loop
from bot.db import Database
from pyrogram import types, filters
import genshinstats as gs

@bot.on_inline_query(filters.regex('characters'))
async def chracters(_, query: types.InlineQuery):
    answers = []
    for character in await loop.run_in_executor(
        None,
        lambda: gs.get_characters(int(Database().find_by_user_id(query.from_user.id)))
    ):
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
        name = f"Traveler({character['element']})" if character['name'] == 'Traveler' else character['name']
        text = f"{element} **{character['name']}** {''.join('⭐️' for _ in range(character['rarity']))}\n"
        text += '=============\n'
        text += f"**Level**: {character['level']}\n"
        text += f"**Friendship**: {character['friendship']}\n"
        text += f"**Constellation**: {character['constellation']}\n"
        if len(character['outfits']) != 0:
            text += f'**Outfit**:\n'
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
                thumb_url=character['icon'].replace(
                    '_image', '_icon',
                ).replace('@2x', ''),
                reply_markup=types.InlineKeyboardMarkup(
                    [
                        [
                            types.InlineKeyboardButton(
                                'Weapon', callback_data=f'w_{character["name"]}_{query.from_user.id}',
                            ),
                            types.InlineKeyboardButton(
                                'Artifacts', callback_data=f'a_{character["name"]}_{query.from_user.id}',
                            ),
                        ],
                        [
                            types.InlineKeyboardButton(
                                'Constellation', callback_data=f'c_{character["name"]}_{query.from_user.id}',
                            ),
                            types.InlineKeyboardButton(
                                'Characters', switch_inline_query_current_chat=f'characters ',
                            ),
                        ],

                    ],
                ),
            ),
        )
    await bot.answer_inline_query(
        query.id,
        results=answers,
        is_gallery=False,
        cache_time=0,
    )