import os
from .conn import SQLITE
from .conn import SQLitePool
from .respone_base import FilesRespone
from .base import File
from datetime import datetime
from .utils import get_file_size, get_wav_info
import uuid

table_name = "files"
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

def query_all_by_page(page=1):
    offset = (int(page) - 1) * limit
    db_pool = SQLitePool(SQLITE)
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    sql = f"""
    SELECT * FROM {table_name}
    LIMIT ? OFFSET ?;
    """
    try:
        cursor.execute(sql, (limit, offset))
        rows = cursor.fetchall()
    except Exception as e:
        return []
    finally:
        db_pool.release_connection(conn)
    return rows

def query_all_by_filename(filename):
    db_pool = SQLitePool(SQLITE)
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    sql = f"""
    SELECT * FROM {table_name}
    WHERE filename = ?;
    """
    try:
        cursor.execute(sql, (filename, ))
        rows = cursor.fetchall()
    except Exception as e:
        return []
    finally:
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

def get_list_respone_json(page=1):
    
    rows = query_all_by_page(page)
    files = []
    
    for row in rows:
        file = {}
        file["filename"] = row[0]
        file["size"] = row[1]
        file["lenght"] = row[2]
        file["text"] = row[3]
        file["create_at"] = row[4]
        file["id"] = row[5]
        file["status"] = row[6]
        file["path"] = row[7]
        files.append(file)
    
    total_page = 0
    localtion_page = page
    
    data_json = {
        "files": files,
        "total_page": total_page,
        "localtion_page": localtion_page
    }
    
    return data_json

def query_insert_voice(filename, size, length, create_at, id):
    db_pool = SQLitePool(SQLITE)
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    sql = f"""
    INSERT INTO {table_name} (filename, size, length, create_at, id)
    VALUES (?, ?, ?, ?, ?)
    """
    try:
        cursor.execute(sql, (filename, size, length, create_at, id))
        conn.commit()
    except Exception as e:
        return False
    finally:
        db_pool.release_connection(conn)
    return True


def upload(file):
    filename = file.filename
    path = os.path.join('data/voices', filename)
    file.save(path)
    size = get_file_size(path)
    length = get_wav_info(path)
    create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    id = str(uuid.uuid4())
    
    if query_all_by_filename(filename) == []:
    
        result = query_insert_voice(filename, size, length, create_at, id)
        if result:
            return {"status": "success"}
        else:
            return {"status": "fail"}
    else:
        return {"status": "exist"}
    