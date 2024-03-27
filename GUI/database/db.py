from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, joinedload
from sqlalchemy import create_engine, MetaData
import redis as redis_db
import GUI.config as config
from ..config import Config


db_url = Config.get_db_url()
print(f'DB URL = {db_url}')
engine = create_engine(db_url, echo=False)


REDIS_HOST = Config.get_redis_host()
REDIS_PORT = Config.get_redis_port()
redis = redis_db.Redis(host=REDIS_HOST, port=REDIS_PORT)


class Base(DeclarativeBase):
    ...


def init_db():
    Base.metadata.create_all(engine)



def drop_db():
    Base.metadata.drop_all(engine)


def drop_redis():
    redis.flushall()
    
