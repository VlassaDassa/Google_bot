import sqlite3






class Database_ref:

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    # EXIST REFERRER
    async def exist_referrer(self, referrer_id):
        with self.connection:
            res = self.cursor.execute('SELECT * FROM `start_registration` WHERE `tgid` = ?', (referrer_id, )).fetchone()
            return res


    # ADD REFERRAL
    async def add_referral(self, referrer_id, referral_id):
        with self.connection:
            self.cursor.execute('INSERT INTO `referral_system` (`referrer`, `referral`) VALUES(?, ?)', (referrer_id, referral_id, ))


    # USERNAME REFERRER'S
    async def username_referrer(self, referrer_id):
        with self.connection:
            return self.cursor.execute('SELECT `user_name` FROM `start_registration` WHERE tgid = ?', (referrer_id, )).fetchone()[0]


    # EXIST REFERRAL IN DB
    async def exist_referral(self, referral_id):
        with self.connection:
            return self.cursor.execute('SELECT `referral` FROM `referral_system` WHERE `referral` = ?', (referral_id, )).fetchone()


    # COUNT REFERRAL
    async def count_referral(self, referrer_id):
        with self.connection:
            return self.cursor.execute('SELECT COUNT(`id`) FROM `referral_system` WHERE referrer = ?', (referrer_id, )).fetchone()[0]






