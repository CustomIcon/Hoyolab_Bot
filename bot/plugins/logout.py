from bot import bot
from pyrogram import filters, types
from bot.db import Database



@bot.on_message(filters.command('logout'))
async def logout_handler(client, message):
    if Database().find_by_user_id(message.from_user.id):
        Database().remove_user_id(message.from_user.id)
        await message.reply(
            "✅ Logged out Successful!"
        )

    else:
        await message.reply("You are not logged in, login using /login command.")