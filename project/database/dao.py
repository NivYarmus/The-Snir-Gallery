import sqlite3

from typing import List, Tuple, Self

from database.constants import DATABASE_PATH
from database.queries import *


class Dao:
    def __init__(self : Self) -> None:
        self.__conn = None
        self.__curr = None

        self.__create_database()
        self.__create_arts_table()

    def __create_database(self : Self) -> None:
        try:
            with open(DATABASE_PATH, 'x'):
                pass
        except:
            pass

    def __create_arts_table(self : Self) -> None:
        self.__execute_query_and_save(CREATE_ARTS_TABLE_QUERY)

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

    def get_arts_intro(self : Self) -> List[Tuple[int, str, str]]:
        return self.__execute_query(GET_ARTS_INTRO_QUERY)

    def get_art(self : Self, name : str) -> List[Tuple[int, str, str, str, int]]:
        return self.__execute_query(GET_ART_BY_NAME_QUERY, name)

    def get_art(self : Self, art_id : int) -> List[Tuple[int, str, str, str, int]]:
        return self.__execute_query(GET_ART_BY_ID_QUERY, art_id)

    def add_art(self : Self, artists : str, name : str, description : str, creation_date : str, is_video_included : bool):
        self.__execute_query_and_save(ADD_ART_QUERY, artists, name, description, creation_date, int(is_video_included))

        return self.__execute_query(GET_MAX_ID_QUERY)

    def get_arts_names(self : Self) -> List[Tuple[int, str]]:
        return self.__execute_query(GET_ARTS_NAMES_QUERY)

    def delete_art(self : Self, art_id : int) -> None:
        self.__execute_query_and_save(DELETE_ART_QUERY, art_id)

    def get_video_status(self : Self, art_id : int) -> None:
        return self.__execute_query(GET_VIDEO_STATUS_QUERY, art_id)

    def edit_art(self : Self, art_id : int, artists : str, name : str, description : str, creation_date : str, is_video_included : bool):
        self.__execute_query_and_save(EDIT_ART_QUERY, artists, name, description, creation_date, int(is_video_included), art_id)
