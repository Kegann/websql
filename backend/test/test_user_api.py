#coding=utf-8
import json
from base64 import b64encode
from test import BaseTestCase
from app.models import User
from app import db

class UserTestCase(BaseTestCase):
    def test_404(self):
        response = self.client.get("/auth/wrong/url")
        self.assertEqual(response.status_code, 404)

    def get_basic_auth_headers(self, username, password):                    
        '''创建Basic Auth认证的headers'''
        return {   
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }          

    def test_get_token(self):
        # 测试登录, 输入正确用户密码获得jwt
        u = User(id=1, name="shen")
        u.set_password("123")
        db.session.add(u)
        db.session.commit()

        # 输入错误密码
        headers = self.get_basic_auth_headers('shen', 'abc')
        response = self.client.post('/auth/login', headers=headers)
        self.assertEqual(response.status_code, 401)

        # 输入正确密码
        headers = self.get_basic_auth_headers('shen', '123')
        response = self.client.post('/auth/login', headers=headers)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('token'))

    def test_not_attach_jwt(self):
        # 测试访问需要用户认证过的api, 不带jwt返回401错误
        response = self.client.post('/sql/history')
        self.assertEqual(response.status_code, 401)

        response = self.client.get('/sql/history')
        self.assertEqual(response.status_code, 401)


    def get_api_headers(self):
        return {             
            'Accept': 'application/json',     
            'Content-Type': 'application/json'
        }                                     


    def test_registry(self):
        # 测试用户注册
        headers = self.get_api_headers()
        # 没有参数,应报400请求错误
        data = json.dumps({})
        response = self.client.post('/auth/user', headers=headers, data=data)
        self.assertEqual(response.status_code, 400)
        # 没有密码pwd, 应报400请求错误
        data = json.dumps({'user': 'shen'})
        response = self.client.post('/auth/user', headers=headers, data=data)
        self.assertEqual(response.status_code, 400)
        # 没有用户名user, 应报400请求错误
        data = json.dumps({'pwd': '123'})
        response = self.client.post('/auth/user', headers=headers, data=data)
        self.assertEqual(response.status_code, 400)
        # 正确提供参数, 应返回201
        data = json.dumps({'pwd': '123', 'user':'shen'})
        response = self.client.post('/auth/user', headers=headers, data=data)
        self.assertEqual(response.status_code, 201)
        # 用户已存在, 应报400请求错误
        data = json.dumps({'pwd': '123', 'user':'shen'})
        response = self.client.post('/auth/user', headers=headers, data=data)
        self.assertEqual(response.status_code, 400)

