from bot import bot, loop
from bot.db import Database
from pyrogram import types, filters
import genshinstats as gs


@bot.on_callback_query(filters.regex('^a_'))
async def artifacts_show(_, query):
    character = query.data.split('_')[1]
    if query.from_user.id != int(query.data.split('_')[2]):
        return await query.answer('This is not your Genshin Impact Account!', show_alert=True)
    for ch in await loop.run_in_executor(None, lambda: gs.get_characters(
        int(
            Database().find_by_user_id(
                query.data.split('_')[2])
            )
        )
    ):
        if ch['name'] == character:
            text = f"**{character}'s Artifacts**\n===============\n"
            if len(ch['artifacts']) == 0:
                return await query.answer('This character has no artifacts!', show_alert=True)
            for art in ch['artifacts']:
                text += f"**[{art['name']}]({art['icon']})** (lvl {art['level']}):\n"
                text += f"Rarity: {''.join('⭐️' for _ in range(art['rarity']))}\n"
                text += f"Set: {art['set']['name']}\n"
                text += "**Effects:**\n"
                for effect in art['set']['effects']:
                    text += f"- {effect['pieces']} - {effect['effect']}\n"
                text += "\n"
            return await query.edit_message_text(
                text,
                disable_web_page_preview=True,
                reply_markup=types.InlineKeyboardMarkup(
                    [[types.InlineKeyboardButton('Go Back', callback_data=f'back_{query.from_user.id}_{character}')]]
                )
            )