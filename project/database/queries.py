"""
    TABLE Arts
    (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Artists TEXT NOT NULL,
        Name TEXT UNIQUE NOT NULL,
        Description TEXT NOT NULL
        Creation_Date TEXT NOT NULL,
        Is_Video_Included INTEGER NOT NULL
    )
"""


CREATE_ARTS_TABLE_QUERY =   """
                            CREATE TABLE IF NOT EXISTS Arts
                            (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Artists TEXT NOT NULL,
                                Name TEXT UNIQUE NOT NULL,
                                Description TEXT NOT NULL,
                                Creation_Date TEXT NOT NULL,
                                Is_Video_Included INTEGER NOT NULL
                            );
                            """

GET_ARTS_QUERY =    """
                    SELECT ID, Name, Description
                    FROM Arts;
                    """

GET_ART_QUERY = """
                SELECT *
                FROM Arts
                WHERE Name = ?;
                """

ADD_ART_QUERY = """
                INSERT INTO
                Arts (Artists, Name, Description, Creation_Date, Is_Video_Included)
                VALUES (?, ?, ? ,?, ?);
                """

GET_MAX_ID_QUERY = """
                    SELECT MAX(ID)
                    FROM Arts;
                    """

GET_ARTS_NAMES_QUERY = """
                        SELECT ID, Name
                        FROM Arts;
                        """

DELETE_ART_QUERY = """
                    DELETE FROM Arts
                    WHERE ID = ?;
                    """

GET_VIDEO_STATUS_QUERY = """
                        SELECT Is_Video_Included
                        FROM Arts
                        WHERE ID = ?;
                        """
