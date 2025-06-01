import sqlite3
from database.config import DB_PATH


def create_table():
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS detectors(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    user_id INTEGER NOT NULL)
""")
    con.close()

def add_detector(name, user_id):
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    cursor.execute(f"""
    INSERT INTO detectors(name, user_id)
    VALUES('{name}', {user_id})
    """)

    con.commit()
    con.close()


def get_detectors(user_id):
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    cursor.execute(f"""
    SELECT id, name FROM detectors
    WHERE user_id = {user_id}
    """)

    detectors = cursor.fetchall()

    con.close()

    return detectors

def delete_detector(id, user_id):
    try:
        int(id)
    except:
        return False

    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    is_deleted = False

    cursor.execute(f"""
    SELECT * FROM detectors
    WHERE user_id = {user_id} AND id = {id}
    """)

    detector = cursor.fetchone()
    if detector:
        cursor.execute(f"""
        DELETE FROM detectors
        WHERE user_id = {user_id} AND id = {id}
        """)
        is_deleted = True

    con.commit()
    con.close()

    return is_deleted


def rename_detector(id, user_id, new_name):
    try:
        int(id)
    except:
        return False

    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    is_renamed = False

    cursor.execute(f"""
        SELECT * FROM detectors
        WHERE user_id = {user_id} AND id = {id}
        """)

    detector = cursor.fetchone()

    if detector:
        cursor.execute(f"""
        UPDATE detectors
        SET name = '{new_name}'
        WHERE id = {id} AND user_id = {user_id}
        """)
        is_renamed = True
    con.commit()
    con.close()
    return is_renamed

def select_all():
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    cursor.execute(f"""
    SELECT * FROM detectors
    """)

    print(cursor.fetchall())
    con.close()

def get_last_detector_id():
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    cursor.execute("""
    SELECT id FROM detectors
    """)

    result = cursor.fetchall()[-1][0]
    con.close()
    return result

def find_user_by_detector_id(id):
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    cursor.execute(f"""
    SELECT user_id FROM detectors
    WHERE id = {id}
    """)

    result = cursor.fetchall()[-1][0]
    if not result:
        raise Exception
    con.close()
    return result

def find_name_by_detector_id(id):
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    cursor.execute(f"""
        SELECT name FROM detectors
        WHERE id = {id}
        """)

    result = cursor.fetchall()[-1][0]
    if not result:
        raise Exception
    con.close()
    return result

if __name__ == '__main__':
    create_table()