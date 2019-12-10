# -*- coding: utf-8 -*-
from test import BaseTestCase
from flask import current_app

class BasicsTestCase(BaseTestCase):
    def test_app_exist(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
