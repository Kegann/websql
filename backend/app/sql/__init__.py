#coding=utf-8
from flask import Blueprint

sql_bp = Blueprint("sql", __name__)

from . import views
