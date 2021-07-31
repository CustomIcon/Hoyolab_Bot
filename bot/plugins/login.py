from bot import bot, loop
from pyrogram import filters, types
from bot.db import Database
import genshinstats as gs


@bot.on_message(filters.command('login'))
async def login_hanler(client, message):
    if len(message.text.split(" ")) > 1:
        if not Database().find_by_user_id(message.from_user.id):
            try:
                await loop.run_in_executor(None, lambda: gs.get_user_stats(int(message.command[1])))
            except gs.errors.AccountNotFound:
                return await message.reply(f"__can't find player with that UID__")
            except gs.errors.DataNotPublic:
                return await message.reply(
                    f"Data is not public, please Login to your hoyolab account, go to profile and make user data public, and you may use /login (UID) once again__",
                    reply_markup=types.InlineKeyboardMarkup(
                        [[types.InlineKeyboardButton('Hoyolab', url='https://hoyolab.com')]]
                    )
                )
            except gs.errors.GenshinStatsException as e:
                return await message.reply(f"__{e}__")
            except ValueError:
                return await message.reply('Which part of UID did you not understand?\nExample: `/login in_game_UID`')
            if Database().find_by_user_uid(message.command[1]):
                return await message.reply(f'Player with UID `{message.command[1]}` already logged in with another Telegram Account!, if this is your real account contact @CustomIcon to get yourself added')
            Database().new_user_id(message.from_user.id, genshin_id=message.command[1])
            await message.reply(
                "✅ Logged in Successful!\nYou can now use the bot via inline",
                reply_markup=types.InlineKeyboardMarkup(
                    [[types.InlineKeyboardButton('Try via Inline', switch_inline_query_current_chat=' ')]]
                )
            )
        else:
            await message.reply('You are already logged in, you can log out with /logout command.')
    else:
        await message.reply("Try logging in with your in-game UID,\nExample: `/login in_game_UID`")