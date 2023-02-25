# 创建sqlalchemy实例
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# 检查文件是否允许上传
import os
from config import IMAGE_ALLOWED_EXTENTIONS


# 检查图片文件是否允许上传
def allowed_file(filename):
    _, ext = os.path.splitext(filename)
    return ext.lower() in IMAGE_ALLOWED_EXTENTIONS
