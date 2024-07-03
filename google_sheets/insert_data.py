from google_sheets.Spreadsheet import Spreadsheet



async def insert_values(cred, spreadsheetId, values, debugMode=False):
    ss = Spreadsheet(cred, spreadsheetId, debugMode=debugMode)

    sheet_title = ss.get_sheet_title(0)  

    async def htmlColorToJSON(htmlColor):
        if htmlColor.startswith("#"):
            htmlColor = htmlColor[1:]
        return {"red": int(htmlColor[0:2], 16) / 255.0, "green": int(htmlColor[2:4], 16) / 255.0,
                "blue": int(htmlColor[4:6], 16) / 255.0}

    read_spreadsheet = ss.service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f"{sheet_title}!A1:C").execute()
    count_rows = len(read_spreadsheet['values'])

    # COORDINATES
    next_row = count_rows + 1
    next_coord = f'A{next_row}:C{next_row}'

    # INSERT VALUES
    ss.prepare_setValues(next_coord, values, sheet_title)
    ss.runPrepared()

    # FORMATTING
    ss.prepare_setCellsFormat(next_coord, {"textFormat": {"fontSize": 12, 'bold': True, "fontFamily": "Comfortaa"}, "horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE"})
    ss.runPrepared()

    # CONDITIONAL FORMATTING
    if int(values[0][1]) == 1:
        ss.prepare_setCellsFormat(next_coord, {"backgroundColor": await htmlColorToJSON("#ff5005")}, fields="userEnteredFormat.backgroundColor")
        ss.runPrepared()

    if int(values[0][1]) == 2:
        ss.prepare_setCellsFormat(next_coord, {"backgroundColor": await htmlColorToJSON("#ba9173")}, fields="userEnteredFormat.backgroundColor")

    if int(values[0][1]) == 3:
        ss.prepare_setCellsFormat(next_coord, {"backgroundColor": await htmlColorToJSON("#ffb961")}, fields="userEnteredFormat.backgroundColor")
        ss.runPrepared()

    if int(values[0][1]) == 4:
        ss.prepare_setCellsFormat(next_coord, {"backgroundColor": await htmlColorToJSON("#8aff8a")}, fields="userEnteredFormat.backgroundColor")
        ss.runPrepared()

    if int(values[0][1]) == 5:
        ss.prepare_setCellsFormat(next_coord, {"backgroundColor": await htmlColorToJSON("#00CC00")}, fields="userEnteredFormat.backgroundColor")
        ss.runPrepared()

    # BORDERS
    column_list = ['A', 'B', 'C']
    for i in column_list:
        border_cord = f'{i}{next_row}:{i}{next_row}'
        ss.prepare_setBorders(border_cord, 5, '#000000')
        ss.runPrepared()







