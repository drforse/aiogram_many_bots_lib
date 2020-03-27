from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from aiomanybots import AioBotsRunner

import asyncio
import logging

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()

# configs
ADMINS = (int, )  # admins ids here (the main bot if set will send status and failure-reports to them)

MAIN_API_TOKEN = 'MAIN_BOT_TOKEN_HERE'
main_storage = MemoryStorage()
main_bot = Bot(MAIN_API_TOKEN)
main_dp = Dispatcher(main_bot, storage=main_storage)

API_TOKEN = 'BOT_TOKEN_HERE'
storage = MemoryStorage()
bot = Bot(API_TOKEN)
dp = Dispatcher(bot, storage=storage)

API_TOKEN_1 = 'BOT_1_TOKEN_HERE'
storage_1 = MemoryStorage()
bot_1 = Bot(API_TOKEN_1)
dp_1 = Dispatcher(bot_1, storage=storage_1)


# your handlers
@main_dp.message_handler(commands=['start'])
async def startbot(m):
    await main_bot.send_message(m.chat.id, 'Привет')


@dp.message_handler(commands=['start'])
async def startbot(m):
    await bot.send_message(m.chat.id, 'Привет')


@dp_1.message_handler(commands=['start'])
async def startbot(m):
    await bot_1.send_message(m.chat.id, 'Привет')

# AioBotRunner configuration

# create AioBotsRunner object
runner = AioBotsRunner(admins=ADMINS, show_traceback=True, loop=loop)

# add all bots you need, main bot should be here too, if not, it won't work
runner.add_bot(name='Первый', bot=bot, dispatcher=dp)
runner.add_bot(name='Second', bot=bot_1, dispatcher=dp_1)
runner.add_bot(name='main', bot=main_bot, dispatcher=main_dp)

# set main bot
runner.set_main_bot(bot=main_bot, dispatcher=main_dp, status_command='status')

# run the bots
runner.run(skip_updates=True)

# run the loop, without it your bots won't work!
loop.run_forever()
