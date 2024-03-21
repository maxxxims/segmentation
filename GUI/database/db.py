from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, joinedload
from sqlalchemy import create_engine, MetaData
import redis as redis_db


db_url = 'sqlite:///GUI/database/database.db'
print(f'DB URL = {db_url}')
engine = create_engine(db_url, echo=False)


redis = redis_db.Redis(host='localhost', port=6379)


class Base(DeclarativeBase):
    ...


def init_db():
    Base.metadata.create_all(engine)



def drop_db():
    Base.metadata.drop_all(engine)


def drop_redis():
    redis.flushall()