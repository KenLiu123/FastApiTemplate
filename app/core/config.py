import yaml


class Config:
    def __init__(self, config_path: str = "config/config.yaml"):
        with open(config_path, 'r', encoding='utf-8') as file:
            self.config = yaml.safe_load(file)

    def get_config(self, key: str):
        keys = key.split('.')   
        value = self.config
        for k in keys:
            value = value.get(k)
        return value or None

settings = Config()

DATABASE_URL = settings.get_config("database.url")
DATABASE_POOL_SIZE = settings.get_config("database.pool_size")

SECRET_KEY = settings.get_config("security.secret_key")
ALGORITHM = settings.get_config("security.algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES = settings.get_config("security.access_token_expire_minutes")   

LOGGING_LEVEL = settings.get_config("logging.level")
LOGGING_FILE = settings.get_config("logging.file")

