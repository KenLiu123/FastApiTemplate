import yaml


class Config:
    def __init__(self, config_path: str = "config/config.yaml"):
        with open(config_path, 'r', encoding='utf-8') as file:
            self.config = yaml.safe_load(file)
            
        # 数据库配置
        self.DATABASE_URL = self.get_config("database.url")
        self.DATABASE_POOL_SIZE = self.get_config("database.pool_size")
        self.DATABASE_MAX_OVERFLOW = self.get_config("database.max_overflow", 10)
        self.DATABASE_POOL_TIMEOUT = self.get_config("database.pool_timeout", 30)
        self.DATABASE_POOL_PRE_PING = self.get_config("database.pool_pre_ping", True)
        
        # 安全配置
        self.SECRET_KEY = self.get_config("security.secret_key")
        self.ALGORITHM = self.get_config("security.algorithm")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = self.get_config("security.access_token_expire_minutes")
            
        # 日志配置
        self.LOGGING_LEVEL = self.get_config("logging.level")
        self.LOGGING_FILE = self.get_config("logging.file")

    def get_config(self, key: str, default=None):
        keys = key.split('.')   
        value = self.config
        for k in keys:
            value = value.get(k)
        return value if value is not None else default

settings = Config()

