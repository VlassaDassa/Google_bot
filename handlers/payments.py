from create_google_bot import bot, dp
from aiogram import types, Dispatcher
from aiogram.types.message import ContentTypes


# FILTERS
from aiogram.dispatcher.filters import Text


# TOKENS
import config as cfg

#DATA BASA
from database.sqlite_payments import Database_pay

PAYMENTS_PROVIDER_TOKEN = cfg.PAYMENTS_PROVIDER_TOKEN


path_db = cfg.PATH_DB
db = Database_pay(path_db)










# Set prices
prices = [
    types.LabeledPrice(label='Доступ', amount=30000),
]


#@dp.message_handler(Text(equals='Купить доступ 💰')
async def cmd_buy(message: types.Message):
    if await db.user_status(message.from_user.id) == 'golden':
        await message.answer('Вы уже приобрели доступ!')
    else:
        await bot.send_invoice(message.chat.id, title='Премиум доступ',
                               description='Доступ ко всем функциям бота',
                               provider_token=PAYMENTS_PROVIDER_TOKEN,
                               currency='RUB',
                               photo_url='https://forchrome.com/wp-content/uploads/2017/01/maxresdefault-5.jpg',
                               photo_height=512,
                               photo_width=512,
                               photo_size=512,
                               prices=prices,
                               start_parameter='ABCD',
                               payload='ABCD')


# ОБРАБОТЧИК ОШИБОК
@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Что-то пошло не так...")


# В СЛУЧАЕ ОПЛАТЫ
#@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    txt_message = f'<b>Поздравляем!</b>\nВы приобрели премиум доступ, теперь вам доступны все функции бота!'
    await db.edit_status(message.from_user.id)


    await bot.send_message(message.chat.id, txt_message, parse_mode='HTML')






def register_handlers_payments(dp: Dispatcher):
    dp.register_message_handler(cmd_buy, Text(equals='Купить доступ 💰'), chat_type='private')
    dp.register_message_handler(got_payment, content_types=ContentTypes.SUCCESSFUL_PAYMENT, chat_type='private')

