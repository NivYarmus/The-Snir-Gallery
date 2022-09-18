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
            IsVideoIncluded INTEGER NOT NULL
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
        (Artists, Name, Description, Creation_Date, IsVideoIncluded)
        VALUES
        ('{name}', '{art}', '{desc}', '{date}', 0);
    """


if __name__ == '__main__':
    conn = sqlite3.connect('./App/database/gallery_dev.db')
    curr = conn.cursor()

    #curr.execute(delete_table())
    #curr.execute(create_db())
    
    conn.commit()

    conn.close()