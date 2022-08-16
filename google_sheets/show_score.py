from google_sheets.Spreadsheet import Spreadsheet

# CONFIG
import config as cfg

# DATABASE
from database.sqlite_client import Database_client


# CREATE OBJECT DB
path_db = cfg.PATH_DB
db = Database_client(path_db)





row = []
def show_score(values, credentials, spreadsheetId):
    ss = Spreadsheet(credentials, spreadsheetId)
    sheet_title = ss.get_sheet_title(0)
    read_spreadsheet = ss.service.spreadsheets().values().get(spreadsheetId=spreadsheetId,
                                                              range=f"{sheet_title}!A1:C").execute()

    for i in range(2):
        read_spreadsheet['values'].pop(0)


    date = values.split('.')
    find_date = '\\'.join(date)


    for i in read_spreadsheet['values']:
        if i[0] == find_date:
            row.append(i)


def return_row():
    return row


def clear_return():
    row.clear()