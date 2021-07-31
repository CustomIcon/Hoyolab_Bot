from bot import bot, loop
from pyrogram import filters, types
from bot.db import Database
import genshinstats as gs


@bot.on_callback_query(filters.regex('^c_'))
async def weapon_show(_, query):
    character = query.data.split('_')[1]
    db = Database()
    uid = db.find_by_user_id(query.data.split('_')[2])
    if query.from_user.id != int(query.data.split('_')[2]):
        return await query.answer('This is not your Genshin Impact Account!', show_alert=True)
    for ch in await loop.run_in_executor(None, lambda: gs.get_characters(int(uid))):
        if ch['name'] == character:
            text = f"**{character}'s Constellations**\n===============\n"
            for con in ch['constellations']:
                prefix = "✅" if con["is_activated"] else "❌"
                text += f'{prefix} **{con["name"]}**\n'
                text += '__{}__\n\n'.format(con["effect"].replace("\\n", " "))
            return await query.edit_message_text(
                text,
                reply_markup=types.InlineKeyboardMarkup(
                    [[types.InlineKeyboardButton('Go Back', callback_data=f'back_{query.from_user.id}_{character}')]]
                )
            )