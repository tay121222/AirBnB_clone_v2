#!/usr/bin/python3
""" """
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


class test_basemodel(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ """
        pass

    def tearDown(self):
        try:
            os.remove('file.json')
        except:
            pass

    def test_kwargs_one(self):
        """ """
        kwargs = {
            'id': '123',
            'created_at': '2023-09-20T12:00:00',
            'updated_at': '2023-09-20T14:00:00',
            'name': 'TestObject',
            'value': 42
        }

    def test_attributes(self):
        """ """
        obj = BaseModel()
        self.assertTrue(hasattr(obj, 'id'))
        self.assertTrue(hasattr(obj, 'created_at'))
        self.assertTrue(hasattr(obj, 'updated_at'))

    def test_save_method(self):
        """ """
        obj = BaseModel()
        old_updated_at = obj.updated_at
        obj.save()
        self.assertNotEqual(old_updated_at, obj.updated_at)

    def test_update_method(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)

if __name__ == '__main__':
    unittest.main()
