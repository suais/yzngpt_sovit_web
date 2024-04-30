from .conn import SQLITE
from .conn import SQLitePool
from .respone_base import SMSRespone
from .base import SMS
from models.aliyunsms import send_sms


table_name = "sms_msgs"
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

def get_list_respone(page=1):
    rows = query_all_by_page(page)
    data = SMSRespone()
    for row in rows:
        sms = SMS()
        sms.uid = row[0]
        sms.username = row[1]
        sms.create_at = row[2]
        sms.msg = row[3]
        sms.phone = row[4]
        sms.id = row[5]
        data.SMSs.append(sms)
    
    data.total_page = 0
    data.localtion_page = page
    return data


def get_list_respone_json(page=1):
    rows = query_all_by_page(page)
    smss = []
    for row in rows:
        sms = {}
        sms["uid"] = row[0]
        sms["username"] = row[1]
        sms["create_at"] = row[2]
        sms["msg"] = row[3]
        sms["phone"] = row[4]
        sms["id"] = row[5]
        smss.append(sms)
    
    total_page = 0
    localtion_page = page
    
    data_json = {
        "smss": smss,
        "total_page": total_page,
        "localtion_page": localtion_page
    }
    
    return data_json

def send_smss():
    send_sms()
    data = {}
    data['msg'] = 'ok'
    return data