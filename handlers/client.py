# AIOGRAM
from create_google_bot import bot, dp
from aiogram import Dispatcher, types

# FSM
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# FILTERS
from aiogram.dispatcher.filters import Text


# KEYBOARD
from keyboard import client_kb as cl_kb

# DATA BASE
from database.sqlite_client import Database_client
from database.sqlite_other import Database_ref
from database.sqlite_payments import Database_pay


# DATETIME
import datetime

# CONFIG
import config as cfg


# GOOGLE SHEET
from google_sheets.insert_data import insert_values
from google_sheets.create_start_sheet import create_start_sheet
from google_sheets.show_score import show_score, return_row, clear_return
from google_sheets import graph as gr

# ASYNCIO
import asyncio


# THREAD
from threading import Thread

# OS
import os


# PERMISSION TO DESCRIBE
from handlers.permission import permission, returns_permission, clear_returns

# RANDOM
from random import randint





# CREATE OBJECT DB
path_db = cfg.PATH_DB
db = Database_client(path_db)
db_ref = Database_ref(path_db)
db_pay = Database_pay(path_db)


# CREDENTIALS
credentials = cfg.PATH_CREDENTIALS


#ANTI FLOOD
async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.answer("Не спешите!")



# START
@dp.throttled(anti_flood, rate=2)
async def start(message: types.Message):
    # SET DEFAULT USER STATUS
    if await db_pay.exist_status(message.from_user.id) is None:
        await db_pay.default_status(message.from_user.id)

    # REFERRAL SYSTEM
    if len(message.text) > 6:

        referrer_id = str(message.text.split(' ')[1])
        if await db_ref.exist_referrer(str(referrer_id)) is not None:

            referrer_name = await db_ref.username_referrer(str(referrer_id))

            if str(referrer_id) == str(message.from_user.id):
                await message.answer('Нельзя регистрироваться по собственной ссылке')

            else:
                if await db_ref.exist_referral(str(message.from_user.id)) is not None:
                    await message.answer(f'Вы уже являетесь рефералом пользователя {referrer_name}')

                else:


                    await db_ref.add_referral(referrer_id, message.from_user.id)

                    # EDIT STATUS
                    if await db_ref.count_referral(referrer_id) >= 10:
                        await db_pay.edit_status(referrer_id)


                    await bot.send_message(message.from_user.id, f'Вы стали рефералом пользователя {referrer_name}!')

                    if message.from_user.username is None:
                        await bot.send_message(referrer_id, f'Пользователь {message.from_user.first_name} ваш новый реферал!')
                    else:
                        await bot.send_message(referrer_id,f'Пользователь {message.from_user.username} ваш новый реферал!')

        else:
            await message.answer('Ссылка недействительна')




    # WELCOME MESSAGE
    welcome_message = f'<b>Приветствую, {message.from_user.first_name}!</b> ✋\nЭтот бот поможет тебе отслеживать' \
                        ' состояние своей жизни с помощью графиков, пометок' \
                        ' и прочих вещей.\nПрисоединяйся!'


    await message.answer(welcome_message, parse_mode='HTML', reply_markup=cl_kb.main_kb)


    # REG USER
    exist_in_db = await db.exist_in_db(message.from_user.id)

    if exist_in_db is None:

        cur_date = datetime.datetime.now().strftime('%Y-%m-%d')

        if message.from_user.username is None:
            await db.reg_user(str(message.from_user.id), str(message.from_user.first_name), str(cur_date))
        else:
            await db.reg_user(str(message.from_user.id), str(message.from_user.username), str(cur_date))




# HELP
async def help(message: types.Message):
    help_message = '<b>Для чего этот бот?</b>\n' \
                   'Благодаря функциям этого бота вы можете:\n' \
                   '• Оценивать свой день\n' \
                   '• Отслеживать и анализировать своё состояние с помощью графиков\n' \
                   '• Получать уникальные советы по поднятию духа\n' \
                   f'\nИскренне надеемся, что вам, {message.from_user.first_name}, поможет один из наших советов!\n' \
                   f'<b>Удачи!</b> ❤' \

    instruction = 'Чтобы начать анализ, необходимо создать <a href="https://www.google.ru/intl/ru/sheets/about/">Google таблицу</a>\n\n' \
                  'И выдать боту разрешение на редактирование:'

    service_gmail = 'Почта, который нужно выдать разрешение: `test-336@nimble-petal-354410.iam.gserviceaccount.com`\n\n' \
                    'Когда вы проделаете все манипуляции, пришлите нам ссылку этой таблицы\n' \
                    '`/set_table` ссылка на таблицу'

    img1 = open(os.path.abspath('assets/1.jpg'), 'rb')
    img2 = open(os.path.abspath('assets/2.jpg'), 'rb')
    
    await message.answer(help_message, parse_mode='HTML', disable_web_page_preview=True)
    await message.answer(instruction, parse_mode='HTML', disable_web_page_preview=True)
    await bot.send_photo(message.from_user.id, img1)
    await bot.send_photo(message.from_user.id, img2)
    await message.answer(service_gmail, parse_mode='MARKDOWN')









# YET
async def yet(message: types.Message):
    await message.delete()
    await message.answer(message.text, reply_markup=cl_kb.secondary_kb)


# MENU
async def menu(message: types.Message):
    await message.delete()
    await message.answer(message.text, reply_markup=cl_kb.main_kb)








# SHOW GRAPH
@dp.throttled(anti_flood, rate=2)
async def show_graph(message: types.Message):
    if await db_pay.user_status(message.from_user.id) == 'golden':
        await message.answer('Выберите за какое количество дней показать график', reply_markup=cl_kb.count_days_graph)
    else:
        await message.answer('Вы ещё не приобрели доступ')



# 10 DAYS GRAPH
@dp.throttled(anti_flood, rate=2)
async def day_10(message: types.Message):
    if await db_pay.user_status(message.from_user.id) == 'golden':
        if await db.exist_spreadsheet(message.from_user.id) is not None:
            await message.answer(message.text, reply_markup=cl_kb.kb_remove)
            await message.delete()
            # START CHECK
            spreadsheetId = await db.get_spreadsheetId(message.from_user.id)
            award = Thread(target=gr.exist_rows, args=(10, spreadsheetId[0], ))     # alive
            award.start()

            await asyncio.sleep(2)

            if await gr.return_answer_exist():
                await gr.remove_list()

                # WAIT...
                collapse_mes = await message.answer('Бот строит график...')
                collapse_sticker = await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAIHvGLD7IfmXUxoiO9RnLPhOSSZy1f2AAIjAAMoD2oUJ1El54wgpAYpBA')

                # START CREATING
                cr_graph = Thread(target=gr.create_graph_, args=(10, spreadsheetId[0],))   # alive
                cr_graph.start()

                await asyncio.sleep(2)

                # DEL WAIT...
                await bot.delete_message(message.from_user.id, collapse_mes.message_id)
                await bot.delete_message(message.from_user.id, collapse_sticker.message_id)


                #RETURN VALUES
                message_dict = gr.return_message_list()
                img = open(message_dict['path'], 'rb')
                await bot.send_photo(message.from_user.id, img)
                os.remove(message_dict['path'])


                # SEND GRAPH
                mes_text = '<b>Краткая характеристика 📋</b>\n' \
                           f'<b>Средняя оценка</b>: {round(message_dict["average"], 2)}\n' \
                           f'<b>Настроение</b>: {message_dict["mood"]}'

                await message.answer(mes_text, parse_mode='HTML', reply_markup=cl_kb.main_kb)

                count_advice = await db.count_advice()
                id_advice = randint(1, count_advice)

                advice_text = '<b>Совет</b>\n' \
                              f'<i>{await db.get_rand_advice(id_advice)}</i>'


                await message.answer(advice_text, parse_mode='HTML')

                gr.clear_message_list()
            else:
                gr.remove_list()
                await message.answer('В вашей таблице пока слишком мало записей')
        else:
            await message.answer('У вас нет таблицы, установите её <b>/set_table</b>', parse_mode='HTML')
    else:
        await message.answer('Вы ещё не приобрели доступ')



# 30 DAYS GRAPH
@dp.throttled(anti_flood, rate=2)
async def day_30(message: types.Message):
    if await db_pay.user_status(message.from_user.id) == 'golden':
        if await db.exist_spreadsheet(message.from_user.id) is not None:
            await message.answer(message.text, reply_markup=cl_kb.kb_remove)
            await message.delete()
            # START CHECK
            spreadsheetId = await db.get_spreadsheetId(message.from_user.id)
            award = Thread(target=gr.exist_rows, args=(30, spreadsheetId[0], ))     # alive
            award.start()

            await asyncio.sleep(2)

            if await gr.return_answer_exist():
                await gr.remove_list()

                # WAIT...
                collapse_mes = await message.answer('Бот строит график...')
                collapse_sticker = await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAIHvGLD7IfmXUxoiO9RnLPhOSSZy1f2AAIjAAMoD2oUJ1El54wgpAYpBA')

                # START CREATING
                cr_graph = Thread(target=gr.create_graph_, args=(30, spreadsheetId[0],))   # alive
                cr_graph.start()

                await asyncio.sleep(2)

                # DEL WAIT...
                await bot.delete_message(message.from_user.id, collapse_mes.message_id)
                await bot.delete_message(message.from_user.id, collapse_sticker.message_id)


                #RETURN VALUES
                message_dict = gr.return_message_list()
                img = open(message_dict['path'], 'rb')
                await bot.send_photo(message.from_user.id, img)
                os.remove(message_dict['path'])


                # SEND GRAPH
                mes_text = '<b>Краткая характеристика 📋</b>\n' \
                           f'<b>Средняя оценка</b>: {round(message_dict["average"], 2)}\n' \
                           f'<b>Настроение</b>: {message_dict["mood"]}'

                await message.answer(mes_text, parse_mode='HTML', reply_markup=cl_kb.main_kb)

                count_advice = await db.count_advice()
                id_advice = randint(1, count_advice)

                advice_text = '<b>Совет</b>\n' \
                              f'<i>{await db.get_rand_advice(id_advice)}</i>'

                await message.answer(advice_text, parse_mode='HTML')

                gr.clear_message_list()
            else:
                await gr.remove_list()
                await message.answer('В вашей таблице пока слишком мало записей')
        else:
            await message.answer('У вас нет таблицы, установите её <b>/set_table</b>', parse_mode='HTML')
    else:
        await message.answer('Вы ещё не приобрели доступ')





# ALL DAYS GRAPH
@dp.throttled(anti_flood, rate=2)
async def all_day(message: types.Message):
    if await db_pay.user_status(message.from_user.id) == 'golden':
        if await db.exist_spreadsheet(message.from_user.id) is not None:
            await message.answer(message.text, reply_markup=cl_kb.kb_remove)
            await message.delete()
            # START CHECK
            spreadsheetId = await db.get_spreadsheetId(message.from_user.id)
            award = Thread(target=gr.exist_rows, args=('all', spreadsheetId[0], ))     # alive
            award.start()

            await asyncio.sleep(2)

            if await gr.return_answer_exist():
                await gr.remove_list()

                # WAIT...
                collapse_mes = await message.answer('Бот строит график...')
                collapse_sticker = await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAIHvGLD7IfmXUxoiO9RnLPhOSSZy1f2AAIjAAMoD2oUJ1El54wgpAYpBA')

                # START CREATING
                cr_graph = Thread(target=gr.create_graph_, args=('all', spreadsheetId[0],))   # alive
                cr_graph.start()

                await asyncio.sleep(2)

                # DEL WAIT...
                await bot.delete_message(message.from_user.id, collapse_mes.message_id)
                await bot.delete_message(message.from_user.id, collapse_sticker.message_id)


                #RETURN VALUES
                message_dict = gr.return_message_list()
                img = open(message_dict['path'], 'rb')
                await bot.send_photo(message.from_user.id, img)
                os.remove(message_dict['path'])


                # SEND GRAPH
                mes_text = '<b>Краткая характеристика 📋</b>\n' \
                           f'<b>Средняя оценка</b>: {round(message_dict["average"], 2)}\n' \
                           f'<b>Настроение</b>: {message_dict["mood"]}'

                await message.answer(mes_text, parse_mode='HTML', reply_markup=cl_kb.main_kb)

                count_advice = await db.count_advice()
                id_advice = randint(1, count_advice)

                advice_text = '<b>Совет</b>\n' \
                              f'<i>{await db.get_rand_advice(id_advice)}</i>'

                await message.answer(advice_text, parse_mode='HTML')


                gr.clear_message_list()
            else:
                await gr.remove_list()
                await message.answer('В вашей таблице пока слишком мало записей')
        else:
            await message.answer('У вас нет таблицы, установите её <b>/set_table</b>', parse_mode='HTML')
    else:
        await message.answer('Вы ещё не приобрели доступ')








# DESCRIPTION DAY
class FSMdescription(StatesGroup):
    score = State()
    description = State()


# START DESCRIBE
@dp.throttled(anti_flood, rate=2)
async def start_description_day(message: types.Message):
    if await db_pay.user_status(message.from_user.id) == 'golden':
        if await db.exist_spreadsheet(message.from_user.id) is not None:
            spreadsheetId = await db.get_spreadsheetId(message.from_user.id)

            #START CHECK
            per = Thread(target=permission, args=(spreadsheetId[0], ))
            per.start()

            # Waiting for the request to returns answer
            await asyncio.sleep(1)

            # Handler errors (wait). If error, then wait and continue
            if returns_permission() == 'Error':

                await asyncio.sleep(1)

                if returns_permission():
                    await clear_returns()
                    await message.answer('Оцените день по шкале от 1 до 5', reply_markup=cl_kb.score_day)
                    await FSMdescription.score.set()
                else:
                    await clear_returns()
                    await message.answer('Сегодня вы уже описывали день, возвращайтесь завтра')

            # If not error, then not wait
            else:
                if returns_permission():
                    await clear_returns()
                    await message.answer('Оцените день по шкале от 1 до 5', reply_markup=cl_kb.score_day)
                    await FSMdescription.score.set()
                else:
                    await clear_returns()
                    await message.answer('Сегодня вы уже описывали день, возвращайтесь завтра')


        else:
            await message.answer('У вас нет таблицы. Установите её `/set_table ссылка на таблицу`', parse_mode='MARKDOWN')

    else:
        await message.answer('Вы ещё не приобрели доступ')




# SCORE
async def score_day(message: types.Message, state: FSMContext):

    try:
        int(message.text)
    except ValueError:
        await message.answer('Введите число от 1 до 5', reply_markup=cl_kb.main_kb)
        await state.finish()
    else:
        if int(message.text) > 5 or int(message.text) < 1:
            await message.answer('Введите число от 1 до 5', reply_markup=cl_kb.main_kb)
            await state.finish()
        else:

            async with state.proxy() as data:
                data['score'] = message.text
                await message.answer('Кратко опишите свой день', reply_markup=cl_kb.kb_remove)

            await FSMdescription.next()



# CHECK
async def check_description_day(message: types.Message, state: FSMContext):
    if len(message.text) > 100:
        len_text = f'Постарайтесь уложиться в 100 символом. Сейчас у вас <b>{len(message.text)}</b> символов'
        await message.answer(len_text, parse_mode='HTML', reply_markup=cl_kb.main_kb)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['description'] = message.text
            check_text = f'<b>Ваш текст:</b>\n"{message.text}"\n<b>Оценка - </b>{data["score"]}'

        await message.answer(check_text, parse_mode='HTML', reply_markup=cl_kb.check_description)
        await FSMdescription.next()


# SAVE DESCRIPTION
async def save_description_day(message: types.Message, state: FSMContext):
    await message.answer('Оценка зачтена в статистику ✔', reply_markup=cl_kb.main_kb)
    async with state.proxy() as data:
        data['date'] = datetime.datetime.now().strftime('%d\\%m\\%Y')

        # Заносимые данные
        values = [[data['date'], data['score'], data['description']]]

        user_spreadsheetId = await db.get_spreadsheetId(message.from_user.id)

        del_mes1 = await message.answer('Подождите, пока бот внесёт данные...', reply_markup=cl_kb.kb_remove)
        del_mes2 = await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAIHvGLD7IfmXUxoiO9RnLPhOSSZy1f2AAIjAAMoD2oUJ1El54wgpAYpBA')

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, run_insert_values, credentials, user_spreadsheetId[0], values)

        await asyncio.sleep(1)

        await message.answer('Данные успешно внесены ✔', reply_markup=cl_kb.main_kb)
        await bot.delete_message(message.from_user.id, del_mes1.message_id)
        await bot.delete_message(message.from_user.id, del_mes2.message_id)

    await state.finish()

def run_insert_values(credentials, spreadsheetId, values):
    asyncio.run(insert_values(credentials, spreadsheetId, values))


# CANCEL
async def cancel(message: types.Message, state: FSMContext):
    await message.answer('Отмена завершена ❌', reply_markup=cl_kb.main_kb)
    await state.finish()


# REFERRAL SYSTEM
async def referral_system(message: types.Message):
    count_referral = await db_ref.count_referral(message.from_user.id)

    if count_referral >= 10:
        msg_text = f'Ссылка: `http://t.me/google_sheets146Bot?start={message.from_user.id}`\n\n' \
                   f'Количество рефералов - {count_referral}\n'
        await message.answer(msg_text, parse_mode='MARKDOWN')

    else:
        msg_text = f'Ссылка: `http://t.me/google_sheets146Bot?start={message.from_user.id}`\n\n' \
                   f'Количество рефералов - {count_referral}\n' \
                   f'Если вы пригласите 10 друзей, то функции бота станут бесплатными'

        await message.answer(msg_text, parse_mode='MARKDOWN')





# SET TABLE
@dp.throttled(anti_flood, rate=2)
async def set_table(message: types.Message):
        if await db.exist_spreadsheet(message.from_user.id) is None:

            if len(message.text) == 10:
                await message.answer('Команда пустая, пришлите ссылку (/set_table <b>ссылка</b>)', parse_mode='HTML')

            else:
                google_link = message.text.split(' ')[1]

                example_link = 'https://docs.google.com/spreadsheets/d/'

                if google_link[0:39] == example_link:
                    spreadsheetId = google_link.split('/')[5]

                    if await db.exist_spreadsheetId(spreadsheetId) is None:



                        del_mes1 = await message.answer('Подождите, пока бот установить таблицу...', reply_markup=cl_kb.kb_remove)
                        del_mes2 = await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAIHvGLD7IfmXUxoiO9RnLPhOSSZy1f2AAIjAAMoD2oUJ1El54wgpAYpBA')


                        create_sheet = Thread(target=await create_start_sheet(credentials, spreadsheetId, message))
                        create_sheet.start()

                        await asyncio.sleep(1)

                        await bot.delete_message(message.from_user.id, del_mes1.message_id)
                        await bot.delete_message(message.from_user.id, del_mes2.message_id)

                    else:
                        await message.answer('Эта таблица уже установлена, пришлите нам ссылку на другую таблицу')

                else:
                    await message.answer('Убедитесь, что это ссылка на таблицу')
        else:
            await message.answer('У вас уже есть установленная таблица', reply_markup=cl_kb.delete_spr)





# DELETE GOOGLE SPREADSHEET
async def delete_spreadsheet(message: types.Message):
    await db.delete_spreadsheet(message.from_user.id)
    await message.answer('Таблица удалена, вы можете установить новую', reply_markup=cl_kb.main_kb)






# SHOW SCORE
class FSMshow_score(StatesGroup):
    date = State()

@dp.throttled(anti_flood, rate=2)
async def start_show_score(message: types.Message):
    if await db_pay.user_status(message.from_user.id) == 'golden':
        if await db.exist_spreadsheet(message.from_user.id) is not None:
            await message.answer('Введите дату за которую хотите узнать оценку:')
            await message.answer('Формат: dd.mm.yy')
            await FSMshow_score.date.set()
        else:
            await message.answer('У вас ещё нет таблицы, установите её <b>/set_table</b>', parse_mode='HTML')
    else:
        await message.answer('Вы ещё не приобрели доступ')


async def show_score_next(message: types.Message, state: FSMContext):
    date = message.text

    # CHECK FORMAT
    try:
        spl_date = date.split('.')
    except:
        await message.answer('Неверный формат даты')
        await state.finish()
    else:
        if len(spl_date)==3:
            for i in spl_date:
                try:
                    int(i)
                except ValueError:
                    await message.answer('Неверный формат даты')
                    await state.finish()

            # FIND
            join_date = '\\'.join(spl_date)
            spreadsheetId = await db.get_spreadsheetId(message.from_user.id)

            # START FIND
            show_score_thread = Thread(target=show_score, args=(join_date, credentials, spreadsheetId[0]))
            show_score_thread.start()


            sticker = await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAIHvGLD7IfmXUxoiO9RnLPhOSSZy1f2AAIjAAMoD2oUJ1El54wgpAYpBA')
            await asyncio.sleep(2)
            await bot.delete_message(message.from_user.id, sticker.message_id)



            # Availability check
            if return_row() == []:
                await message.answer('Ничего не найдено')
            else:
                values = return_row()[0]
                mes_text = f'<b>Дата:</b> {values[0]}\n' \
                           f'<b>Оценка:</b> {values[1]}\n' \
                           f'<b>Описание:</b> {values[2]}\n'

                await message.answer(mes_text, parse_mode='HTML')
                clear_return()
            await state.finish()

        else:
            await message.answer('Неверный формат даты')
            await state.finish()






# REGISTRATION
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], chat_type='private')
    dp.register_message_handler(help, Text(equals='Помощь 🔎'), chat_type='private')
    dp.register_message_handler(yet, Text(equals='Ещё ➡'), chat_type='private')
    dp.register_message_handler(menu, Text(equals='Меню 💤'), chat_type='private')
    dp.register_message_handler(referral_system, Text(equals='Реферальная система 👥'), chat_type='private')

    # GRAPH
    dp.register_message_handler(show_graph, Text(equals='График состояния 📈'), chat_type='private')
    dp.register_message_handler(day_10, Text(equals='10 📈'), chat_type='private')
    dp.register_message_handler(day_30, Text(equals='30 📈'), chat_type='private')
    dp.register_message_handler(all_day, Text(equals='За всё время 📈'), chat_type='private')

    # DESCRIPTION DAY
    dp.register_message_handler(start_description_day, Text(equals='Описать день 📝'), chat_type='private', state=None)
    dp.register_message_handler(cancel, Text(equals='❌'), chat_type='private', state='*')
    dp.register_message_handler(score_day, chat_type='private', state=FSMdescription.score)
    dp.register_message_handler(check_description_day, chat_type='private', state=FSMdescription.description)
    dp.register_message_handler(save_description_day, Text(equals='Сохранить ✔'), chat_type='private')
    dp.register_message_handler(start_description_day, Text(equals='Изменить ✏'), chat_type='private')
    # SHOW SCORE
    dp.register_message_handler(start_show_score, Text(equals='Показать оценку 🔢'), state = None, chat_type='private')
    dp.register_message_handler(show_score_next, chat_type='private', state = FSMshow_score.date)

    # SET SPREADSHEET
    dp.register_message_handler(set_table, Text(contains='/set_table'), chat_type='private')
    # DELETE SPREADSHEET
    dp.register_message_handler(delete_spreadsheet, Text(equals='Удалить таблицу'), chat_type='private')

