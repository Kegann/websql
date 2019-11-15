#coding=utf-8
import os
from pyhive import hive
from app import create_app, db
from app.models import User

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


@app.before_first_request
def create_admin():
    print("First request in ...")
    db.drop_all()
    db.create_all()
    user = User()
    user.name = 'admin'
    user.set_password("123456@E")
    db.session.add(user)
    db.session.commit()

if __name__ =="__main__":
    app.run(debug=True, host="0.0.0.0", port=24802)
