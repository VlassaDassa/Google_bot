import sqlite3






class Database_pay:

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()


    # EXIST
    async def exist_status(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM `user_status` WHERE tgid = ?', (user_id, )).fetchone()


    # ADD DEFAULT STATUS
    async def default_status(self, user_id):
        with self.connection:
            self.cursor.execute('INSERT INTO `user_status` (`tgid`, `status`) VALUES(?, ?)', (user_id, 'default', ))


    # EXIST REFERRER
    async def edit_status(self, user_id):
        with self.connection:
            self.cursor.execute('UPDATE `user_status` SET status = ? WHERE tgid = ?', ('golden', user_id, ))


    # CHECK STATUS
    async def user_status(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT `status` FROM `user_status` WHERE tgid = ?', (user_id, )).fetchone()[0]