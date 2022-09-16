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
            Artists TEXT NOT NULL,
            Name TEXT UNIQUE NOT NULL,
            Description TEXT NOT NULL,
            Creation_Date TEXT NOT NULL,
            IsVideoIncluded INTEGER NOT NULL
        );
    """


def insert_art():

    name = "Artist(s)"
    art = "Art name"
    desc = "Art description"
    date = "Art creation date"

    return f"""
        INSERT INTO Arts
        (Artists, Name, Description, Creation_Date, IsVideoIncluded)
        VALUES
        ('{name}', '{art}', '{desc}', '{date}', 0);
    """


if __name__ == '__main__':
    conn = sqlite3.connect('./App/database/gallery.db')
    curr = conn.cursor()

    #curr.execute(delete_table())
    #curr.execute(create_db())
    #curr.execute(insert_art())

    curr.execute("""
        UPDATE Arts
        SET IsVideoIncluded = 1
        WHERE ID = 1;
    """)
    
    conn.commit()

    conn.close()