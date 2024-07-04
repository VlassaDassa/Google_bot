# Google_Bot


## Функционал
Работа с Google Sheets
- Ежедневная оценка текущего дня;
- Анализ диапазона дней (10, 30, все) при помощи построенных графиков;
- Тестовая система оплаты;
- Запланированное уведомление пользователей; 

## Инструкция по использованию
В разделе "Помощь 🔎" имеется инструкция по применению:

![image](https://github.com/VlassaDassa/Google_Bot/assets/107307197/248f0f6b-7b3b-43ec-869d-00ba8d35e5b3)

## Стэк
python==3.9.7, aiogram, matplotlib, gsheets

## Инструкция по установке
```sh
python -m venv venv
venv\Scripts\activate
pip install -r .\requirements.txt
python manage.py app.py
```

## Инструкция по разработке
В файле config.py существуют переменные для настройки и комментарии к ним.

Все необходимые токены можно получить у BotFather, а для системы оплаты в Юкасса



