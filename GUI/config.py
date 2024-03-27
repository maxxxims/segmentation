


class Config:
    @classmethod
    def get_gui_host(cls):
        return '0.0.0.0'
    @classmethod
    def get_gui_port(cls):
        return 8050
    @classmethod
    def get_db_url(cls):
        return 'sqlite:///GUI/database/database.db'
    @classmethod
    def get_redis_host(cls):
        return 'localhost'
    @classmethod
    def get_redis_port(cls):
        return 6379