from .conn import SQLITE
from .conn import SQLitePool
from .respone_base import RecordRespone
from .base import Record

table_name = "record"
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
    data = RecordRespone()
    
    for row in rows:
        record = Record()
        record.filename = row[0]
        record.length = row[1]
        record.size = row[2]
        record.text = row[3]
        record.uid = row[4]
        record.create_at = row[5]
        record.id = row[6]
        record.path = row[7]
        data.records.append(record)
    
    data.total_page = 0
    data.localtion_page = page
    
    return data

def get_list_respone_json(page=1):
    
    rows = query_all_by_page(page)
    records = []
    
    for row in rows:
        record = {}
        record["filename"] = row[0]
        record["length"] = row[1]
        record["size"] = row[2]
        record["text"] = row[3]
        record["uid"] = row[4]
        record["create_at"] = row[5]
        record["id"] = row[6]
        record["path"] = row[7]
        records.append(record)
    
    total_page = 0
    localtion_page = page
    
    data_json = {
        'records': records,
        'total_page': total_page,
        'localtion_page': localtion_page
    }
    
    return data_json