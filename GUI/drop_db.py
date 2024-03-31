from .database.db import drop_redis, drop_db

if __name__ == '__main__':
    drop_redis()
    drop_db()