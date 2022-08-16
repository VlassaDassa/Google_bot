from google_sheets.Spreadsheet import Spreadsheet
import googleapiclient.errors

import config as cfg
from database.sqlite_client import Database_client

from keyboard import client_kb as cl_kb

path_db = cfg.PATH_DB
db = Database_client(path_db)



# COLOR
async def create_start_sheet(GOOGLE_CREDENTIALS_FILE, spreadsheetId, message, debugMode=False):
    try:
        def htmlColorToJSON(htmlColor):
            if htmlColor.startswith("#"):
                htmlColor = htmlColor[1:]
            return {"red": int(htmlColor[0:2], 16) / 255.0, "green": int(htmlColor[2:4], 16) / 255.0,
                    "blue": int(htmlColor[4:6], 16) / 255.0}



        sheetTitle = "Оценка дня"


        header = [['Оценка дня. Анализ состояния']]
        header_1 = [['Дата', 'Оценка', 'Краткое описание']]


        rowCount = 100000


        # CREATING AN INSTANCE OF A CLASS
        ss = Spreadsheet(GOOGLE_CREDENTIALS_FILE, spreadsheetId, debugMode=debugMode)

        # ADDING A NEW SHEET
        ss.addSheet(sheetTitle, rows=rowCount + 3, cols=8)



        # EDITING SIZE CELL
        ss.prepare_setRowHeight(0 ,40)
        ss.prepare_setRowsHeight(1, rowCount +3, 40)
        ss.prepare_setColumnWidth(2, 200)
        ss.prepare_setColumnWidth(1, 200)


        # FORMATTING TEXT
        ss.prepare_setCellsFormat("A1:B1", {'backgroundColor': htmlColorToJSON('#9988DD'), "textFormat": {"fontSize": 11, 'bold': True, "fontFamily": "Comfortaa"},  "horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE"})
        ss.prepare_setCellsFormat("A2:C2", {'backgroundColor': htmlColorToJSON('#ffb829'), "textFormat": {"fontSize": 12, "bold": True, "fontFamily": "Comfortaa"}, "horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE"})


        # BORDERS
        ss.prepare_setBorders("A1:B1", 5, "#000000")



        columns_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        # HEADER BORDERS
        i = 0
        while i != 3:
            ss.prepare_setBorders(f'{columns_list[i]}2:{columns_list[i]}2', 5, '#000000')
            i += 1



        ss.prepare_mergeCells("A1:B1")



        # START TASK
        ss.rename_Spreadsheet('Анализ состояния')  # --> переименование
        list_id = ss.get_sheet_id(0)               # id листа
        ss.deleteSheet(int(list_id))               # удаление листа по id



        # INSERT VALUES
        sheet_title = ss.get_sheet_title(0)

        ss.prepare_setValues("A1:B1", header, sheet_title)
        ss.prepare_setValues("A2:C2", header_1, sheet_title)

        ss.runPrepared()

        await message.answer('Таблица успешно создана ✔', reply_markup=cl_kb.main_kb)
        await db.set_table(message.from_user.id, spreadsheetId)

    except googleapiclient.errors.HttpError:
        mes_text = 'Вы не выдали разрешение на редактирование боту: `test-336@nimble-petal-354410.iam.gserviceaccount.com`'
        await message.answer(mes_text, parse_mode='MARKDOWN')
