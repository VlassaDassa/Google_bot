# AIOGRAM
from aiogram.utils import executor
from create_google_bot import dp, bot
from aiogram.utils.exceptions import BotBlocked

# HANDLERS
from handlers import client, payments

# APSCHEDULER
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# CONFIG
import config as cfg

# DATABASE
from database.sqlite_client import Database_client

# PLANNED DESCRIPTION
from google_sheets.planned_description import planned_description

# THREAD
from threading import Thread

# OS
import os




# CREATE OBJECT DB
path_db = cfg.PATH_DB
db = Database_client(path_db)




API_TOKEN = cfg.TOKEN
WEBHOOK_HOST = 'https://vlasadasa.ru'
WEBHOOK_PATH = f'/{cfg.TOKEN}/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
print(WEBHOOK_URL)



async def notification():
    mes_text = '<b>Привет!</b> 👋\n' \
               'Время уже 21:00, если ты ещё не описал свой день,\n' \
               'то самое время это сделать!\n\n' \
               '<b>Удачи</b> ❤'

    list_user_id = await db.get_user_id()

    for i in list_user_id:

        try:
            await bot.send_message(i[0], mes_text, parse_mode='HTML')
        except BotBlocked:
            pass

#'http:/147.78.65.30/webhook/5568123217:AAGc2Wuts1pm5c_DI4LrBUYkcY7La7olvNA' <-- это стяло в вебхукюрл, може тпригодится не знаю


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    print(' Бот вышел в онлайн\n')
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    # NOTIFICATION
    scheduler.add_job(notification, 'cron', hour=21, minute=0)
    scheduler.start()


async def on_shutdown(dp):
    await bot.delete_webhook()




def run_planned_description():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(planned_description, 'cron', hour=23, minute=50)
    scheduler.start()

thread = Thread(target=run_planned_description())
thread.start()




client.register_handlers_client(dp)
payments.register_handlers_payments(dp)




executor.start_webhook(
    dispatcher=dp,
    webhook_path=WEBHOOK_PATH, 
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host="localhost",
    port=8443
)




























