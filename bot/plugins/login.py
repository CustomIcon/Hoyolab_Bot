from bot import bot, loop
from pyrogram import filters, types
from bot.db import Database
import genshinstats as gs
from bot.utils import strings


@bot.on_message(filters.command('login'))
async def login_hanler(client, message):
    if len(message.text.split(' ')) > 1:
        if not Database().find_by_user_id(message.from_user.id):
            try:
                await loop.run_in_executor(
                    None,
                    lambda: gs.get_user_stats(int(message.command[1])),
                )
            except gs.errors.AccountNotFound:
                return await message.reply(strings.PlayerNotFound)
            except gs.errors.DataNotPublic:
                return await message.reply(
                    strings.DataNotPublic,
                    reply_markup=types.InlineKeyboardMarkup(
                        [[
                            types.InlineKeyboardButton(
                                'Hoyolab', url='https://hoyolab.com',
                            ),
                        ]],
                    ),
                )
            except gs.errors.GenshinStatsException as e:
                return await message.reply(f'__{e}__')
            except ValueError:
                return await message.reply(strings.UIDNotFound)
            if Database().find_by_user_uid(message.command[1]):
                return await message.reply(
                    strings.UIDExists.format(message.command[1]),
                )
            Database().new_user_id(
                message.from_user.id,
                genshin_id=message.command[1],
            )
            await message.reply(
                strings.LoginSuccess,
                reply_markup=types.InlineKeyboardMarkup(
                    [[
                        types.InlineKeyboardButton(
                            'Try via Inline',
                            switch_inline_query_current_chat=' ',
                        ),
                    ]],
                ),
            )
        else:
            await message.reply(
                strings.AlreadyLoggedIn,
            )
    else:
        await message.reply(
            strings.LoginTry,
        )
