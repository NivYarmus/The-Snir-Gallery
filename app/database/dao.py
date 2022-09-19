import sqlite3

from typing import List, Tuple, Self

from .constants import DATABASE_PATH
from .queries import *


class Dao:
    def __init__(self : Self) -> None:
        self.__conn = None
        self.__curr = None

        self.__create_arts_table()

    def __open_db(self : Self) -> None:
        self.__conn = sqlite3.connect(DATABASE_PATH)
        self.__curr = self.__conn.cursor()

    def __close_db(self : Self) -> None:
        self.__curr = None
        self.__conn.close()

    def __execute_query(self : Self, query : str, *args : List[str]) -> None:
        self.__open_db()
        result = self.__curr.execute(query, args).fetchall()
        self.__close_db()

        return result

    def __execute_query_and_save(self : Self, query : str, *args : List[str]) -> None:
        self.__open_db()
        result = self.__curr.execute(query, args).fetchall()
        self.__save_changes()
        self.__close_db()

        return result

    def __save_changes(self : Self) -> None:
        self.__conn.commit()
    
    def __create_arts_table(self : Self) -> None:
        self.__execute_query_and_save(CREATE_ARTS_TABLE_QUERY)

    def get_arts(self : Self) -> List[Tuple[int, str, str]]:
        return self.__execute_query(GET_ARTS_QUERY)

    def get_art(self : Self, name : str) -> List[Tuple[int, str, str, str, int]]:
        return self.__execute_query(GET_ART_QUERY, name)
