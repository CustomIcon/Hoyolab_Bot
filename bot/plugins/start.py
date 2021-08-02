from bot import bot
from pyrogram import filters, types
from bot.utils import strings


@bot.on_message(
    filters.command('start', prefixes='/'),
)
async def start_command(_, message: types.Message):
    await message.reply(
        strings.start,
    )
