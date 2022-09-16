import sqlite3


class Dao:
    """
        TABLE Arts (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Artists TEXT NOT NULL,
            Name TEXT UNIQUE NOT NULL,
            Description TEXT NOT NULL
            Creation_Date TEXT NOT NULL,
            IsVideoIncluded INTEGER NOT NULL
        )
    """

    DATABASE_PATH = './database/gallery.db'

    def __init__(self):
        self.__conn = None
        self.__curr = None
    
    def __open_db(self):
        self.__conn = sqlite3.connect(Dao.DATABASE_PATH)
        self.__curr = self.__conn.cursor()
    
    def __close_db(self):
        self.__curr = None
        self.__conn.close()
    
    def __execute_query(self, query, *args):
        self.__open_db()
        result = self.__curr.execute(query, args).fetchall()
        self.__close_db()

        return result
    
    def get_arts(self):
        query = """
            SELECT ID, Name, Description
            FROM Arts;
        """

        return self.__execute_query(query)
    
    def get_art(self, name):
        query = """
            SELECT *
            FROM Arts
            WHERE Name = ?;
        """

        return self.__execute_query(query, name)