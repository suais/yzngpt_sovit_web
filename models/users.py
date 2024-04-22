import uuid
from .conn import SQLITE
from .conn import SQLitePool
from .respone_base import UsersRespone
from .base import Users
import datetime
from models.utils import generate_uid

table_name = "users"
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
    except Exception:
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
    except Exception:
        return []
    finally:
        db_pool.release_connection(conn)
    return rows


def query_all_by_username(username):
    db_pool = SQLitePool(SQLITE)
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    sql = f"""
    SELECT * FROM {table_name}
    WHERE username = ?;
    """
    try:
        cursor.execute(sql, (username,))
        rows = cursor.fetchall()
    except Exception:
        return []
    finally:
        db_pool.release_connection(conn)
    return rows


def query_all_by_username_uid(username, uid):
    db_pool = SQLitePool(SQLITE)
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    sql = f"""
    SELECT * FROM {table_name}
    WHERE username = ?
    AND uid = ?;
    """
    try:
        cursor.execute(sql, (username, uid))
        rows = cursor.fetchall()
    except Exception:
        return []
    finally:
        db_pool.release_connection(conn)
    return rows

def query_all_by_uid(uid):
    db_pool = SQLitePool(SQLITE)
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    sql = f"""
    SELECT * FROM {table_name}
    WHERE uid = ?;
    """
    try:
        cursor.execute(sql, (uid,))
        rows = cursor.fetchall()
    except Exception:
        return []
    finally:
        db_pool.release_connection(conn)
    return rows 

def query_all_by_username_pwd(username, password):
    db_pool = SQLitePool(SQLITE)
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    sql = f"""
    SELECT * FROM {table_name}
    WHERE username = ?
    AND password = ?;
    """
    try:
        cursor.execute(sql, (username, password))
        rows = cursor.fetchall()
    except Exception:
        return []
    finally:
        db_pool.release_connection(conn)
    return rows 

def query_insert_user(uid, username, email, password, is_admin):
    db_pool = SQLitePool(SQLITE)
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    sql = f"""
    INSERT INTO {table_name} (uid, username, email, password, is_admin)
    VALUES (?, ?, ?, ?, ?)
    """
    try:
        cursor.execute(sql, (uid, username, email, password, is_admin))
        conn.commit()
    except Exception as e:
        return False
    finally:
        db_pool.release_connection(conn)
    return True

def query_update_user(uid, username, email, password):
    db_pool = SQLitePool(SQLITE)
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    sql = f"""
    UPDATE {table_name}
    SET username = ?, email = ?, password = ?
    WHERE uid = ?;
    """
    try:
        cursor.execute(sql, (username, email, password, uid))
        conn.commit()
    except Exception as e:
        return False
    finally:
        db_pool.release_connection(conn)
    return True

def query_update_login_time(username):
    db_pool = SQLitePool(SQLITE)
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    curret_time =datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = f"""
    UPDATE {table_name}
    SET last_login = ?
    WHERE username = ?;
    """
    try:
        cursor.execute(sql, (curret_time, username))
        conn.commit()
    except Exception as e:
        return False
    finally:
        db_pool.release_connection(conn)
    return True


def new_user(username, email, password, is_admin):
    uid = generate_uid()
    is_uid_exist = query_all_by_uid(uid) == []
    is_username_exist = query_all_by_username(username) ==[]
    is_email_empty = email == ""
    is_password_empty = password == ""
    
    if is_uid_exist and is_username_exist and not is_password_empty:
        query_insert_user(uid, username, email, password, is_admin)
        return True
    else:
        return False
    

def edit_user(uid, username, email, password):
    is_username_exist_self = query_all_by_username_uid(username, uid) == []
    print(is_username_exist_self)
    if not is_username_exist_self:
        query_update_user(uid, username, email, password)
        return True
    else:
        is_username_exist = query_all_by_username(username) == []
        if is_username_exist:
            query_update_user(uid, username, email, password)
            return True
        else:
            return False

    
def new_user_json(username, email, password, is_admin="0"):
    result = new_user(username, email, password, is_admin)
    if result:
        return {"status": "success"}
    else:
        return {"status": "fail"}
    
def edit_user_json(uid, username, email, password):
    result = edit_user(uid, username, email, password)
    if result:
        return {"status": "success"}
    else:
        return {"status": "fail"}

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


def user_auth(username, password):
    result = query_all_by_username_pwd(username=username, password=password)
    if result == []:
        return False
    else:
        return True
    

def api_user_info_json(username):
    result = query_all_by_username(username)
    data = {}
    data['info'] = {}
    if result != []:
        for row in result:
            data['info']['username'] = row[0]
            data['info']['email'] = row[1]
            data['info']['last_login'] = row[3]
            data['info']['uid'] = row[4]
        data['msg'] = 'ok'
    else:
         data['msg'] = 'filed'
    return data
    
        
def admin_auth(username):
    result = query_all_by_username(username)
    if result != []:
        for row in result:
            is_admin = row[6]
    else:
        is_admin = "0"
    return is_admin
    
