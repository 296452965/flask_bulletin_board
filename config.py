import os

basedir = os.path.abspath(os.path.dirname(__file__))
HOST = os.environ.get('HOST')
PORT = os.environ.get('PORT')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')
CHARSET = os.environ.get('CHARSET')

# 上传配置
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
MAX_CONTENT_LENGTH = 128 * 1024 * 1024  # 128MB


class BaseConfig:
    # SQLALCHEMY配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class DevelopmentConfig(BaseConfig):
    SECRET_KEY = 'dev'
    DEBUG = True
    DATABASE = 'cyk_flask'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?{}'.format(USER, PASSWORD, HOST, PORT, DATABASE, CHARSET)
    SQLALCHEMY_DATABASE_URI = DB_URI


class TestingConfig(BaseConfig):
    SECRET_KEY = 'test'
    DATABASE = 'cyk_flask_test'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?{}'.format(USER, PASSWORD, HOST, PORT, DATABASE, CHARSET)
    SQLALCHEMY_DATABASE_URI = DB_URI


class ProductionConfig(BaseConfig):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE = 'cyk_flask'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?{}'.format(USER, PASSWORD, HOST, PORT, DATABASE, CHARSET)
    SQLALCHEMY_DATABASE_URI = DB_URI


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

