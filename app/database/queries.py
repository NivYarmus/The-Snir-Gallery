"""
    TABLE Arts
    (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Artists TEXT NOT NULL,
        Name TEXT UNIQUE NOT NULL,
        Description TEXT NOT NULL
        Creation_Date TEXT NOT NULL,
        IsVideoIncluded INTEGER NOT NULL
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
                                IsVideoIncluded INTEGER NOT NULL
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