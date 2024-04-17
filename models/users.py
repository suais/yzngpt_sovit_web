from .conn import SQLITE
from .conn import SQLitePool
from .respone_base import UsersRespone
from .base import Users


table_name = "users"
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
    data = UsersRespone()
    
    for row in rows:
        user = Users()
        user.username = row[0]
        user.email = row[1]
        user.password = row[2]
        user.last_login = row[3]
        user.uid = row[4]
        user.status = row[5]
        user.is_admin = row[6]
        data.users.append(user)
    
    data.total_page = 0
    data.localtion_page = page
    
    return data

def get_list_respone_json(page=1):
    rows = query_all_by_page(page)
    users = []
    for row in rows:
        user = {}
        user['username'] = row[0]
        user["email"] = row[1]
        user["password"] = row[2]
        user["last_login"] = row[3]
        user["uid"] = row[4]
        user["status"] = row[5]
        user["is_admin"] = row[6]
        users.append(user)
    
    total_page = 0
    localtion_page = page
    
    json_data = {
        "users": users,
        "total_page": total_page,
        "localtion_page": localtion_page
    }
    
    return json_data
