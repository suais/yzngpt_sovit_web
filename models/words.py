from .conn import SQLITE
from .conn import SQLitePool
from .respone_base import WordsRespone
from .base import Words
import datetime

table_name = "words"
limit = 20

def query_all():
    db_pool = SQLitePool(SQLITE)
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    sql = f"""
    SELECT * FROM {table_name}
    """
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        return []
    finally:
        db_pool.release_connection(conn)
    return rows

def query_update_words(text):
    db_pool = SQLitePool(SQLITE)
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    id = "01"
    edit_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    sql = f"""
    UPDATE {table_name}
    SET text = ?, edit_at = ?
    WHERE id = ?;
    """
    try:
        cursor.execute(sql, (text, edit_at, id))
        conn.commit()
    except Exception as e:
        return False
    finally:
        db_pool.release_connection(conn)
    return True


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

def get_words():
    result = query_all()
    words = []
    for row in result:
        word = {}
        word["text"] = row[0]
        word['edit_at'] = row[1]
        word['id'] = row[2]
        words.append(word)
    
    json_data = {
        "words": words
    }
        
    return json_data


def edit_words(text):
    result = query_update_words(text)
    if result:
        return {"status": "success"}
    else:
        return {"status": "fail"}