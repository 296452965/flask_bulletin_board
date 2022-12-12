from flask import Blueprint

bp = Blueprint('login', __name__, url_prefix='/')

from .views import *
