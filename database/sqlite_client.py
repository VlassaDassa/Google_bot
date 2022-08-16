import sqlite3


class Database_client:

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()


    # SELECT USER ID
    async def get_user_id(self):
        with self.connection:
            return self.cursor.execute(
                'SELECT `tgid` FROM `start_registration`'
            ).fetchall()


    # EXIST IN DB
    async def exist_in_db(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM `start_registration` WHERE tgid = ?', (user_id, )).fetchone()


    # REG USER
    async def reg_user(self, user_id, user_name, date_reg):
        with self.connection:
            self.cursor.execute('INSERT INTO `start_registration` (`user_name`, `tgid`, `date_reg`) VALUES (?, ?, ?)',
                                (user_name, user_id, date_reg, ))





    # EXIST SPREADSHEET ID
    async def exist_spreadsheetId(self, spreadsheetId):
        with self.connection:
           return self.cursor.execute('SELECT * FROM `google_id` WHERE spreadsheetId = ?', (spreadsheetId, )).fetchone()



    # SET TABLE
    async def set_table(self, user_id, spreadsheetId):
        with self.connection:
            self.cursor.execute('INSERT INTO `google_id` (`tgid`, `spreadsheetId`) VALUES (?, ?)',
                                (user_id, spreadsheetId))


    # EXIST SPREADSHEET
    async def exist_spreadsheet(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM `google_id` WHERE tgid = ?', (user_id, )).fetchone()


    # EXIST ALL SPREADSHEET
    async def exist_all_spreadsheet(self):
        with self.connection:
            res = self.cursor.execute('SELECT COUNT(`spreadsheetId`) FROM `google_id`').fetchone()
            return bool(res[0])


    # SPREADSHEETID
    async def get_spreadsheetId(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT `spreadsheetId` FROM `google_id` WHERE tgid = ?', (user_id, )).fetchone()


    # DELETE SPREADSHEET
    async def delete_spreadsheet(self, user_id):
        with self.connection:
            self.connection.execute('DELETE FROM `google_id` WHERE tgid = ?', (user_id, ))


    # LIST ALL SPREADSHEET ID
    async def get_all_spreadsheetId(self):
        with self.connection:
            return self.cursor.execute(
                'SELECT `spreadsheetId` FROM `google_id`'
            ).fetchall()


    # COUNT ADVICE
    async def count_advice(self):
        with self.connection:
            res = self.connection.execute('SELECT COUNT(`advice`) FROM `advice`').fetchall()
            return res[0][0]


    # GET RANDOM ADVICE
    async def get_rand_advice(self, id):
        with self.connection:
            res = self.connection.execute('SELECT `advice` FROM `advice` WHERE id = ?', (id, )).fetchone()
            return res[0]





