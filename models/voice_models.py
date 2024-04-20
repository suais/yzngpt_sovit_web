from .conn import SQLITE
from .conn import SQLitePool
from .respone_base import FilesRespone
from .base import File
from datetime import datetime

table_name = "models"

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