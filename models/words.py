from .conn import SQLITE
from .conn import SQLitePool
from .respone_base import WordsRespone
from .base import Words


table_name = "words"
limit = 20

def query_all():
    db_pool = SQLitePool(SQLITE)
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    sql = f"""
    SELECT * FROM {table_name}
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    db_pool.release_connection(conn)
    return rows


def get_list_respone():
    
    rows = query_all()
    data = WordsRespone()
    
    for row in rows:
        words = Words()
        words.id = row[2]
        words.text = row[0]
        words.edit_at = row[1]
        data.words.append(words)
    
    return data
