# DATETIME
import datetime

# Google
from google_sheets.Spreadsheet import Spreadsheet


# CONFIG
import config as cfg






per_list = []

def permission(spreadsheet_Id):
    # CURRENT TIME
    cur_date = datetime.datetime.now().strftime('%Y-%m-%d')


    # READ SHEET
    spreadsheetId = spreadsheet_Id
    ss = Spreadsheet(cfg.PATH_CREDENTIALS, spreadsheetId)
    sheet_title = ss.get_sheet_title(0)
    read_spreadsheet = ss.service.spreadsheets().values().get(spreadsheetId=spreadsheetId,
                                                              range=f"{sheet_title}!A1:C").execute()

    all_row = read_spreadsheet['values']

    for i in (range(0,2)):
        all_row.pop(0)

    user_row = all_row

    if user_row == []:
        per_list.append(True)
    else:
        last_row = user_row[-1]

        # COMPARE
        date = last_row[0]
        day = date.split('\\')[0]
        cur_day = cur_date.split('-')[-1]


        # Можно поменять местами и за один день можно будет сделать много записей
        if cfg.ONE_ROW_IN_DAY:
            if int(cur_day) != int(day) :
                per_list.append(True)
            else:
                per_list.append(False)
        else:
            per_list.append(False)




# RETURN PERMISSION
def returns_permission():
    # Error handler
    if per_list == []:
        return 'Error'

    else:
        return per_list[0]

# CLEAR LIST
async def clear_returns():
    per_list.clear()
