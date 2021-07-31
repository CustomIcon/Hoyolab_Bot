from bot import bot, loop
from pyrogram import filters, types
from bot.db import Database
import genshinstats as gs

@bot.on_callback_query(filters.regex('^back_'))
async def back_btn(_, query):
    if query.from_user.id == int(query.data.split('_')[1]):
        db = Database()
        uid = db.find_by_user_id(query.data.split('_')[1])
        for character in await loop.run_in_executor(None, lambda: gs.get_characters(int(uid))):
            if query.data.split('_')[2] == character['name']:
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
                text = f"{element} **{character['name']}** {''.join('⭐️' for _ in range(character['rarity']))}\n"
                text += "=============\n"
                text += f"**Level**: {character['level']}\n"
                text += f"**Friendship**: {character['friendship']}\n"
                text += f"**Constellation**: {character['constellation']}\n"
                if len(character['outfits']) != 0:
                    text += f"**Outfit**:\n"
                    for outfit in character['outfits']:
                        text += f"- {outfit['name']}\n"
                return await query.edit_message_text(
                    text,
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
    else:
        await query.answer('This is not your Genshin Impact Account!', show_alert=True)