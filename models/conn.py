import sqlite3
import threading

SQLITE = "data/sqlite/zn_voice.db"

class SQLitePool:
    def __init__(self, db_path, pool_size=10):
        self.db_path = db_path
        self.pool = []
        self.lock = threading.Lock()
        for _ in range(pool_size):
            conn = sqlite3.connect(db_path)
            self.pool.append(conn)

    def get_connection(self):
        self.lock.acquire()
        if len(self.pool) > 0:
            conn = self.pool.pop()
            self.lock.release()
            return conn
        else:
            self.lock.release()
            raise Exception("Connection pool is empty")

    def release_connection(self, conn):
        self.lock.acquire()
        self.pool.append(conn)
        self.lock.release()

# # 使用示例
# db_pool = SQLitePool('example.db')

# # 从连接池中获取连接
# conn = db_pool.get_connection()

# # 执行SQL语句
# cursor = conn.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
# cursor.execute("INSERT INTO users (name) VALUES (?)", ('Alice',))
# conn.commit()

# # 释放连接
# db_pool.release_connection(conn)