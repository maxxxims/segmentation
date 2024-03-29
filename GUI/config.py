import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    @classmethod
    def get_gui_host(cls):
        return os.getenv('GUI_HOST')
    @classmethod
    def get_gui_port(cls):
        return os.getenv('GUI_PORT')
    @classmethod
    def get_db_url(cls):
        return os.getenv('DB_URL')
    @classmethod
    def get_redis_host(cls):
        return os.getenv('REDIS_HOST')
    @classmethod
    def get_redis_port(cls):
        return os.getenv('REDIS_PORT')
    @classmethod
    def get_redis_login(cls):
        return 'redis'
    @classmethod
    def get_redis_password(cls):
        return os.getenv('REDIS_PASSWORD')
    @classmethod
    def get_tutorial_url(cls):
        return os.getenv('TUTORIAL_URL')