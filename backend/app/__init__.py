#coding=utf-8
from flask import Flask
from config import config
from app.sql import sql_bp
from app.extensions import cors

def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # 不检查路由中最后是否有斜杠/
    app.url_map.strict_slashes = False

    register_blueprints(app)
    register_extensions(app)
    app.app_context().push()
    return app

def register_blueprints(app):
    app.register_blueprint(sql_bp, url_prefix="/sql")

def register_extensions(app):
    cors.init_app(app)
