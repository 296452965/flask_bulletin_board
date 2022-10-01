# 数据库的配置变量
HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'cyk_flask'
USERNAME = 'root'
PASSWORD = 'root'
CHARSET  = 'charset=utf8mb4'
DB_URI   = 'mysql+pymysql://{}:{}@{}:{}/{}?{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE, CHARSET)

# SQLALCHEMY配置
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

# 项目配置
DEBUG = True
SECRET_KEY = "sdfadan13!@fjflo0#2!"

# 上传配置
UPLOAD_FOLDER = r'C:\Users\Chengyikang\PycharmProjects\bulletin_board\uploads'
MAX_CONTENT_LENGTH = 128 * 1024 * 1024  # 128MB
