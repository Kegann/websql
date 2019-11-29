#coding=utf-8
from app.auth import auth_bp
from flask import jsonify, request, g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.errors import error_response
from app.models import User
from app.extensions import db

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

def get_jwt():
    pass

@auth_bp.route("/", methods=['GET'])
def test():
    return "AUTH: HELLO WORLD..."

@basic_auth.verify_password
def verify_password(username, password):
    # print("USERNAME: {}, PASSWD: {}".format(username, password))
    user = User.query.filter_by(name=username).first()
    if not user:
        return False
    g.current_user = user
    return user.check_password(password)

@token_auth.verify_token
def verify_token(token):
    # print ("\nToken: {}".format(token))
    g.current_user = User.verify_jwt(token) if token else None
    g.current_token = token
    return g.current_user is not None

@basic_auth.error_handler
def basic_auth_error():
    return error_response(401, "username or password is invalid.")

@token_auth.error_handler
def token_auth_erro():
    return error_response(401, "not login or invalid token.")

@auth_bp.route("/login", methods=['POST'])
@basic_auth.login_required
def login():
    token = g.current_user.get_jwt()
    g.current_token = token
    return jsonify({"code": 200, "data": "login succeed!", 'token': token})

@auth_bp.route("/user", methods=['POST'])
def register():
    try:
        name = request.get_json().get('user')
        pwd = request.get_json().get('pwd')
        if not ( name and pwd ):
            return error_response(400, "invalid username or passwd...")
        user = User()
        user.name = name
        user.set_password(pwd)
        db.session.add(user)
        db.session.commit()
        token = user.get_jwt()
        g.current_token = token
        return jsonify({"code": 201, "data": "register succeed!" ,"token":
                        token})
    except Exception as err:
        return error_response(500, "sth bad happened...")
    return error_response(500, "sth bad happened...")
