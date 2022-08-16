from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove








#MAIN KEYBOARD
but1 = KeyboardButton('Помощь 🔎')
but2 = KeyboardButton('Описать день 📝')
but3 = KeyboardButton('График состояния 📈')
yet = KeyboardButton('Ещё ➡')
main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.row(but1, but2).row(but3,yet)


# SECONDARY KEYBOARD
btn1 = KeyboardButton('Показать оценку 🔢')
btn2 = KeyboardButton('Реферальная система 👥')
btn3 = KeyboardButton('Купить доступ 💰')
menu = KeyboardButton('Меню 💤')
secondary_kb = ReplyKeyboardMarkup(resize_keyboard=True)
secondary_kb.row(btn1, btn2).row(btn3, menu)



# KEYBOARD REMOVE
kb_remove = ReplyKeyboardRemove()



#COUNT DAYS GRAPH
b1 = KeyboardButton('10 📈')
b2 = KeyboardButton('30 📈')
b3 = KeyboardButton('За всё время 📈')
count_days_graph = ReplyKeyboardMarkup(resize_keyboard=True)
count_days_graph.row(b1,b2,b3).add(menu)



# SCORE DAY
a1 = KeyboardButton('1')
a2 = KeyboardButton('2')
a3 = KeyboardButton('3')
a4 = KeyboardButton('4')
a5 = KeyboardButton('5')
cancel = KeyboardButton('❌')
score_day = ReplyKeyboardMarkup(resize_keyboard=True)
score_day.row(a1, a2, a3).row(a4, a5, cancel)



# CHECK DESCRIPTION
check1 = KeyboardButton('Сохранить ✔')
check2 = KeyboardButton('Изменить ✏')
check_description = ReplyKeyboardMarkup(resize_keyboard=True)
check_description.row(check1, check2).add(cancel)



# DELETE GOOGLE SPREADSHEET
del_spr = KeyboardButton('Удалить таблицу')
delete_spr = ReplyKeyboardMarkup(resize_keyboard=True)
delete_spr.row(del_spr, menu)