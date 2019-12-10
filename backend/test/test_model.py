#coding=utf-8
from test import BaseTestCase
from app.models import Sql, User
from app import db

class ModelTestCase(BaseTestCase):
    def test_sql_model(self):
        sql = Sql()
        sql.id = 1
        sql.content = "test..."
        sql.res = "test..."
        db.session.add(sql)
        db.session.commit()
        self.assertEqual(Sql.query.filter_by(id=1).first().content, "test...")

    def test_user_model(self):
        user = User()
        user.name = 'test'
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.check_password('123456'))
        self.assertFalse(user.check_password('123pass'))

    def test_user_sqls(self):
        # 测试sql外键指定user
        user = User(name="shen", id=1)
        user.set_password("123")
        sql = Sql(content="321", res="456")
        self.assertEqual(user.sqls.all(), [])
        sql.user_id = 1
        db.session.add(user)
        db.session.add(sql)
        db.session.commit()
        self.assertFalse(len(user.sqls.all()) == 0)
        self.assertEqual(user.sqls.all()[0].content, "321")
        self.assertEqual(user.sqls.all()[0].res, "456")
