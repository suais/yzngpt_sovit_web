from .conn import SQLITE
from .conn import SQLitePool
from .respone_base import UserOnlineRespone
from .base import UserOnline
import datetime
from models.users import query_all_by_username

table_name = "user_online_tmp"

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


def query_del_passed(uid): # 删掉过期登录数据
    db_pool = SQLitePool(SQLITE)
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    sql = f"""
    DELETE FROM {table_name}
    WHERE uid = ?;
    """
    try:
        cursor.execute(sql,(uid,))
        conn.commit()
    except Exception as e:
        return False
    finally:
        db_pool.release_connection(conn)
    return True


def query_expired_login():
    result = query_all()
    curret_time = datetime.datetime.now()
    for row in result:
        uid = row[0]
        login_time = row[2]
        login_time = datetime.datetime.strptime(login_time, "%Y-%m-%d %H:%M:%S")
        time_diff = abs(curret_time - login_time)
        if time_diff.total_seconds() > 20:
            query_del_passed(uid)
            return True
        else:
            False

def query_insert(uid, username, login_time):
    db_pool = SQLitePool(SQLITE)
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    sql = f"""
    INSERT OR REPLACE INTO {table_name} (uid, username, login_time)
    VALUES (?, ?, ?);
    """
    try:
        cursor.execute(sql, (uid, username, login_time))
        conn.commit()
    except Exception as e:
        return False
    finally:
        db_pool.release_connection(conn)
    return True


def respone():
    rows = query_all()
    data = UserOnlineRespone()

    for row in rows:
        user_online = UserOnline()
        user_online.uid = row[0]
        user_online.username = row[1]
        user_online.time = row[2]
        data.users.append(user_online)
    return data


def online(username):
    data = {}
    query_uid = query_all_by_username(username)
    if query_uid != []:
        uid = query_uid[0][4]
        print(query_uid)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query_insert(uid, username, time)
        result = query_expired_login()
        data['msg'] = 'ok'
        return data
    else:
        data['msg'] = 'filed'
        return data