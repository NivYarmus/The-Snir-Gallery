import sqlite3


def delete_table():
    return """
        DROP TABLE Arts;
    """

def delete_item(id):
    return f"""
        DELETE FROM Arts
        WHERE ID = {id};
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
            Is_Video_Included INTEGER NOT NULL
        );
    """


def insert_art(n):
    val = str(n)

    name = val
    art = val
    desc = val
    date = val

    return f"""
        INSERT INTO Arts
        (Artists, Name, Description, Creation_Date, Is_Video_Included)
        VALUES
        ('{name}', '{art}', '{desc}', '{date}', 0);
    """


if __name__ == '__main__':
    conn = sqlite3.connect('./project/database/gallery.db')
    curr = conn.cursor()

    curr.execute(delete_item(23))
    
    conn.commit()

    conn.close()