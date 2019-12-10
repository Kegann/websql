# -*- coding: utf-8 -*-
import unittest
from app import create_app, db

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        # 创建并推送上下文
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()
        self.client = self.app.test_client() # flask内建客户端, 模拟浏览器行为

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()
