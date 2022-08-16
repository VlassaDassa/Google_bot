from google_sheets.Spreadsheet import Spreadsheet

# DATE
import datetime

# CONFIG
import config as cfg

# DATABASE
from database.sqlite_client import Database_client

# INSERT VALUES
from google_sheets.insert_data import insert_values





# CREATE OBJECT DB
path_db = cfg.PATH_DB
db = Database_client(path_db)

# CREDENTIALS
credentials = cfg.PATH_CREDENTIALS





async def planned_description():
    print('Началось плановое описание!')
    # CURRENT DATE
    cur_date = datetime.datetime.now().strftime('%Y-%m-%d')

    if await db.exist_all_spreadsheet():

        # LIST SPREADSHEET ID
        list_spreadsheetId = await db.get_all_spreadsheetId()


        # READ SHEET
        for spreadsheet_id in list_spreadsheetId:
            spreadsheetId = spreadsheet_id[0]
            ss = Spreadsheet(cfg.PATH_CREDENTIALS, spreadsheetId)
            sheet_title = ss.get_sheet_title(0)
            read_spreadsheet = ss.service.spreadsheets().values().get(spreadsheetId=spreadsheetId,
                                                                      range=f"{sheet_title}!A1:C").execute()

            all_row = read_spreadsheet['values']
            last_row = all_row[-1][0]

            cur_day = cur_date.split('-')[-1]
            user_day = last_row.split('\\')[0]

            if cur_day != user_day:

                date_values = datetime.datetime.now().strftime('%d\%m\%Y')
                values = [[date_values, 'Пусто', 'Пусто']]
                print('Внос данных...')
                insert_values(credentials, spreadsheetId, values)

        print('Плановое описание завершено!')
    else:
        print('ПЛАНОВОЕ ОПИСАНИЕ: Ни одной таблицы нет!')

