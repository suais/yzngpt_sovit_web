from .conn import SQLITE
from .conn import SQLitePool
from .respone_base import UserOnlineRespone
from .base import UserOnline


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


def respone():
    rows = query_all()
    data = UserOnlineRespone()
    for row in rows:
        user_online = UserOnline()
        user_online.uid = row[0]
        user_online.username = row[1]
        user_online.login_time = row[2]
        user_online.login_length = row[3]
        data.users.append(user_online)
    return data




