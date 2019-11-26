#coding=utf-8
import jwt
from flask import current_app
from datetime import datetime, timedelta
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Sql(db.Model):
    __tablename__ = "Sql_history"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    res = db.Column(db.Text)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    passwd_hash = db.Column(db.String(256))
    authority = db.Column(db.Integer)
    sqls = db.relationship('Sql', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.passwd_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwd_hash, password)

    def get_jwt(self, expires_in=1800):
        '''用户登录后，发放有效的JWT'''
        now = datetime.utcnow()
        payload = {
            'user_id': self.id,
            'user_name': self.name,
            'exp': now + timedelta(seconds=expires_in)
        }
        print("produce: ", payload['exp'])
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_jwt(token):
        '''验证JWT的有效性'''
        try:
            payload = jwt.decode(
                token,
                current_app.config.get('SECRET_KEY'),
                algorithm=['HS256']
            )
        except (jwt.exceptions.ExpiredSignatureError,
                jwt.exceptions.InvalidSignatureError,
                jwt.exceptions.DecodeError) as e:
            # Token过期， 或被人修改， 验证也会失败
            return None
        return User.query.get(payload.get('user_id'))
