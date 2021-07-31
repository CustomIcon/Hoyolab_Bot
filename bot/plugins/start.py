from bot import bot
from pyrogram import filters, types


@bot.on_message(
    filters.command("start", prefixes='/')
)
async def start_command(_, message: types.Message):
    await message.reply(
        'This bot is currently under Development,\n\n**Available Commands:**\n- /login - login to your hoyolab account\n- /logout - log out from the bot'
        )
