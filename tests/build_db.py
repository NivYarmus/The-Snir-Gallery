import sqlite3


def delete_table():
    return """
        DROP TABLE Arts;
    """


def create_db():
    return """
        CREATE TABLE IF NOT EXISTS Arts
        (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Artist TEXT NOT NULL,
            Name TEXT UNIQUE NOT NULL,
            Description TEXT,
            Creation_Date TEXT NOT NULL
        );
    """


def insert_art():

    name = "ניב ירמוס"
    art = "היצירה שלי"
    desc = "תיאור היצירה שלי"
    date = "14-09-2022"

    return f"""
        INSERT INTO Arts
        (Artist, Name, Description, Creation_Date)
        VALUES
        ('{name}', '{art}', '{desc}', '{date}');
    """


if __name__ == '__main__':
    conn = sqlite3.connect('./App/database/arts.db')
    curr = conn.cursor()

    #curr.execute(delete_table())
    curr.execute(create_db())
    #curr.execute(insert_art())

    #curr.execute("""UPDATE Arts SET Description = 'בלה בלה בלה בלה בלה בלה בלה בלה בלה בלה בלה בלה בלה בלה בלה בלה בלה בלה בלה בלה בלה' where ID = 1;""")
    conn.commit()

    conn.close()