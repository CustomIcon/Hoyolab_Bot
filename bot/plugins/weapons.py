from bot import bot, loop
from pyrogram import filters
from bot.db import Database
import genshinstats as gs


@bot.on_callback_query(filters.regex('^w_'))
async def weapon_show(client, query):
    character = query.data.split('_')[1]
    for ch in await loop.run_in_executor(
        None, lambda: gs.get_characters(
            int(Database().find_by_user_id(query.data.split('_')[2])),
        ),
    ):
        if ch['name'] == character:
            wep = ch['weapon']
            text = f'{wep["name"]} ({wep["type"]})\n'
            text += f"Rarity: {''.join('⭐️' for _ in range(wep['rarity']))}\n"
            text += f"Lvl: {wep['level']}\n"
            text += f"Ascension: {wep['ascension']}\n"
            text += f"Refinement: {wep['refinement']}\n"
            return await query.answer(text, show_alert=True)
