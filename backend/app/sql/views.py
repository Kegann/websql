#coding=utf-8
from . import sql_bp
from flask import jsonify, request, g, url_for
from app.errors import error_response
from pyhive import hive
from app.auth.views import token_auth
from app.models import Sql
from app.extensions import db

def result_format(header, data):
    res = []
    for i in range(len(data)):
        sub_ele = {}
        for j in range(len(header)):
            sub_ele[header[j][0]] = data[i][j]
        res.append(sub_ele)
    # print ("RES: ", res)
    return res

def query_carbon(sql_line,host="10.17.0.62", port=10000):
    thrift_conn = hive.Connection(host=host, port=port,
                                  database="default")
    thrift_cursor = thrift_conn.cursor()
    thrift_cursor.execute(sql_line)
    # print("RES: ", thrift_cursor.description)
    res = {}
    header = thrift_cursor.description
    data = thrift_cursor.fetchall()
    res['header'] = header
    res['data'] = result_format(header, data)
    return res

@sql_bp.route("/", methods=['POST','GET'])
def query():
    sql_line = eval(request.get_data(as_text=True)).get('sql_line')
    if not sql_line:
        return jsonify({"res":""})
    res = query_carbon(sql_line)
    #print("Response: ", res['data'])
    return jsonify({"res":res})

@sql_bp.route("/history", methods=['POST'])
@token_auth.login_required
def save_sql():
    false = False
    null = None
    true = True
    # print("REQUEST: ", request.get_data(as_text=False))
    req = eval(request.get_data(as_text=True))
    sql_line = req.get('sql_line')
    sql_res = str(req.get('sql_res'))
    user_id = g.current_user.id
    # print ("SAVE : ", sql_line, user_id)
    if sql_line:
        sql = Sql()
        sql.content = sql_line
        sql.user_id = user_id
        sql.res = sql_res
        db.session.add(sql)
        db.session.commit()
        return jsonify({"code": 201, "data": "save succeed!"})
    # 没有从请求中获取到要保存的sql将语句，认为该请求有错误
    return jsonify({"code": 400, "data": "request not acceptable..."})

@sql_bp.route("/history", methods=['GET'])
@token_auth.login_required
def get_sqls():
    user_id = g.current_user.id
    sqls = Sql.query.filter_by(user_id=user_id).all()
    sql_history = []
    for i in sqls:
        try:
            sql_res = eval(i.res)
            sql_history.append({"sql_line":i.content, "create_time": i.create_time,
                                "sql_res": sql_res})
            # print("Sql_RES: ", sql_res, type(sql_res))
        except Exception as err:
            print(err)
    return jsonify({"code": 200, "data": "get sqls succeed!", "sqls":
                    sql_history})

