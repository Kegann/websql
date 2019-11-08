#coding=utf-8
import os
from pyhive import hive
from app import create_app

app = create_app(os.getenv("FLASK_CONFIG") or "default")

@app.route("/", methods=['GET'])
def index():
    res = query_carbon("show tables")
    print("RES: ", res)
    return "Hello world"

def query_carbon(sql_line,host="10.17.0.62", port=10000):
    thrift_conn = hive.Connection(host=host, port=port,
                                  database="default")
    thrift_cursor = thrift_conn.cursor()
    thrift_cursor.execute(sql_line)
    res = thrift_cursor.fetchall()
    return res

if __name__ =="__main__":
    app.run(debug=True, host="0.0.0.0", port=24802)
