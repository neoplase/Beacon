import sqlite3


class Database:

    def __init__(self):
        self.Path = ''
        self.Connection = None

    def Create_Database(self, Path):

        try:
            self.Path = Path
            conn = sqlite3.connect(Path)
            self.Connection = conn

            return True
        except sqlite3.Error as e:
            print(e)

        return False

    def Create_Table(self, SQLQuery):
        try:
            c = self.Connection.cursor()
            c.execute(SQLQuery)
        except sqlite3.Error as e:
            print(e)

    def GetQuery(self, SQLQuery):
        if self.Connection != None :
            cur = self.Connection.cursor()
            cur.execute(SQLQuery)
            rows = cur.fetchall()

            return rows

        return None