'''
Unit test module for functions in tddb.py
'''

# pylint: disable=C0305
# pylint: disable=R0904


import unittest

import tddb as tb

from collections.abc import Iterable


class TestTB(unittest.TestCase):
    '''
    Class definition for unit tests for main.py
    '''

    def setUp(self):
        '''
        Test initialization of todo collection
        '''
        self.todo_col = tb.ToDoCollection()
        self.assertIsInstance(
            self.todo_col,
            tb.ToDoCollection,
            msg="Returned object not todo_collection"
        )


    def test_add_todo(self):
        new_todo = self.todo_col.add_todo( "capra", "capra_0007", "HBO Max ads...:-P" )
        self.assertTrue( new_todo )

    def test_search_todo(self):
        new_todo = self.todo_col.add_todo( "bmeau", "bmeau_0008", "Netflix ads as well" )
        self.assertTrue( new_todo )
        todo = self.todo_col.search_todo( "bmeau_0008" )
        self.assertEqual( todo.todo_text, "Netflix ads as well" )

    def test_modify_todo(self):
        new_todo = self.todo_col.add_todo( "pfram", "pfram_0001", "I prefer Disney" )
        self.assertTrue( new_todo )
        mod_success = self.todo_col.modify_todo( "pfram_0001", "pfram", "I heart Disney" )
        self.assertTrue( mod_success )

    def test_delete_todo(self):
        new_todo = self.todo_col.add_todo( "jimmypage", "jimmypage_0002", "BBC for me" )
        self.assertTrue( new_todo )
        del_success = self.todo_col.delete_todo( "jimmypage_0002" )
        self.assertTrue( del_success )
        #
        # See if we can find the todo we deleted
        #
        todo = self.todo_col.search_todo( "jimmypage_0002" )
        self.assertIsNone( todo )

    def test_search_all_todo_updates(self):
        new_todo = self.todo_col.add_todo( "maddrox", "maddrox_0008", "Netflix ads as well" )
        self.assertTrue( new_todo )
        new_todo = self.todo_col.add_todo( "maddrox", "maddrox_0009", "Amazon Prime has no ads" )
        self.assertTrue( new_todo )
        todo_list = self.todo_col.search_all_todo_updates( "maddrox" )
        self.assertIsInstance( todo_list, list )

    def test_filter_todo_by_string(self):
        new_todo = self.todo_col.add_todo( "lukec", "lukec_0008", "Netflix hosts my show" )
        self.assertTrue( new_todo )
        new_todo = self.todo_col.add_todo( "lukec", "lukec_0009", "Amazon Prime is too lame to host my show" )
        self.assertTrue( new_todo )
        todo_iterator = self.todo_col.filter_todo_by_string( "host" )
        self.assertIsInstance( todo_iterator, Iterable )
        self.assertEquals( len( [ stat.todo_text for stat in todo_iterator ] ), 2 )


# --- END --- #

