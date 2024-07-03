import asyncio
from threading import Thread
from aiogram.utils import executor
from create_google_bot import dp, bot
from aiogram.utils.exceptions import BotBlocked
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers import client, payments
import config as cfg
from database.sqlite_client import Database_client
from google_sheets.planned_description import planned_description

# CREATE OBJECT DB
path_db = cfg.PATH_DB
db = Database_client(path_db)

API_TOKEN = cfg.TOKEN

# Webhook
WEBHOOK_PATH = f'/{cfg.TOKEN}/'
WEBHOOK_URL = f"{cfg.WEBHOOK_HOST}{WEBHOOK_PATH}"

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

async def on_startup(dp):
    print('Бот вышел в онлайн\n')
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    # NOTIFICATION
    scheduler.add_job(notification, 'cron', hour=21, minute=0)
    scheduler.start()

async def on_shutdown(dp):
    await bot.delete_webhook()

def run_planned_description():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(planned_description, 'cron', hour=23, minute=50)
    scheduler.start()
    loop.run_forever()

thread = Thread(target=run_planned_description)
thread.start()

client.register_handlers_client(dp)
payments.register_handlers_payments(dp)

if __name__ == '__main__':
    variant_start = input('Variant start:\n1. Long polling;\n2. Webhook\nYour choice: ')

    if variant_start == '1':
        executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)

    elif variant_start == '2':
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH, 
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host="localhost",
            port=8443
        )
    else:
        print("Invalid choice. Please enter 1 for Long polling or 2 for Webhook.")
