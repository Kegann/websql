#coding=utf-8
import os
import jwt
import time
import click
from datetime import datetime
from pyhive import hive
from flask import current_app, g, jsonify
from app import create_app, db
from app.models import User

app = create_app(os.getenv("FLASK_CONFIG") or "default")

@app.cli.command()
def hello():
    click.echo('say-hello')

@app.route("/", methods=['GET'])
def index():
    res = query_carbon("show tables")
    # print("RES: ", res)
    return "Hello world"

def query_carbon(sql_line,host="10.17.0.62", port=10000):
    thrift_conn = hive.Connection(host=host, port=port,
                                  database="default")
    thrift_cursor = thrift_conn.cursor()
    thrift_cursor.execute(sql_line)
    res = thrift_cursor.fetchall()
    return res


# 首次请求来时创建表和管理员用户
@app.before_first_request
def create_admin():
    print("First request in ...")
    # db.drop_all()
    db.create_all()
    user_exist = User.query.filter_by(name="admin").all()
    print("USERS: ", user_exist)
    if not user_exist:
        print("user_exist: ", user_exist)
        user = User()
        user.name = 'admin'
        user.set_password("123456")
        db.session.add(user)
        db.session.commit()

# 每次请求结束时尝试更新token
@app.after_request
def after_request(response):
    resp_json = response.get_json()
    # print("RESP_JSON: ", resp_json)
    try:
        # token = resp_json.get('token')
        token = g.current_token
        payload = jwt.decode(
            token,
            current_app.config.get('SECRET_KEY'),
            algorithm=['HS256']
        )
        exp = payload.get('exp')
        now = time.mktime(datetime.utcnow().timetuple())
        # print("EXP: {}, NOW: {}...".format(exp, now))
        # 默认token离过期5min内更新
        update_period = os.getenv('TOKEN_UPDATE_PERIOD',  5)
        if now + int(update_period) * 60 >= exp:
            new_token = g.current_user.get_jwt()
            resp_json['token'] = new_token
            return jsonify(resp_json)
    except Exception as err:
        print("EXCEPTION: ", err)
        return response
    return response

if __name__ =="__main__":
    app.run(debug=True, host="0.0.0.0", port=24802)
