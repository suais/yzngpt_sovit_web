from .conn import SQLITE
from .conn import SQLitePool
from .respone_base import FilesRespone
from .base import File


table_name = "files"
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

def query_all_by_page(page=1):
    offset = (int(page) - 1) * limit
    
    db_pool = SQLitePool(SQLITE)
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    sql = f"""
    SELECT * FROM {table_name}
    LIMIT ? OFFSET ?;
    """
    cursor.execute(sql, (limit, offset))
    rows = cursor.fetchall()
    db_pool.release_connection(conn)
    return rows

def get_list_respone(page=1):
    
    rows = query_all_by_page(page)
    data = FilesRespone()
    
    for row in rows:
        file = File()
        file.filename = row[0]
        file.size = row[1]
        file.lenght = row[2]
        file.text = row[3]
        file.create_at = row[4]
        file.id = row[5]
        file.status = row[6]
        file.path = row[7]
        data.files.append(file)
    
    data.total_page = 0
    data.localtion_page = page
    
    return data
