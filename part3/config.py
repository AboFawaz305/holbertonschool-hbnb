import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    API_URL = "http://127.0.0.1:5000"


config = {"development": DevelopmentConfig, "default": DevelopmentConfig}
