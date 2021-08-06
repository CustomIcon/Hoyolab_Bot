from bot import bot
from pyrogram import filters, types
from bot.db import Database
from bot.utils import strings


@bot.on_message(filters.command('logout'))
async def logout_handler(_, message: types.Message):
    if Database().find_by_user_id(message.from_user.id):
        Database().remove_user_id(message.from_user.id)
        await message.reply(
            strings.LoggedOutSuccess,
        )

    else:
        await message.reply(strings.NotLoggedIn)
