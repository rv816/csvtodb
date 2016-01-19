#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_csvtodb
----------------------------------

Tests for `csvtodb` module.
"""

import unittest

from csvtodb.csvtodb import * 


class TestCsvtodb(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

testfix = [['foo', 'bar', 'yellow'], ['thing1', 'thing2', 3], ['green', 'purple', 10]]
def test_upload_to_db():
    db_url = 'sqlite://'
    db = dataset.connect(db_url)
    tablename = 'qrs_valueset_to_codes'
    testtable = upload_to_db(testfix, tablename, db_url)
    assert list(testtable.all())[1]['foo'] == 'green'

