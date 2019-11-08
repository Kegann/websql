#coding=utf-8
from . import sql_bp
from flask import jsonify, request, g, url_for
from app.errors import error_response
from pyhive import hive

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
