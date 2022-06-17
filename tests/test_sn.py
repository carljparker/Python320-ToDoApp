'''
Unit test module for functions in main.py
'''

# pylint: disable=C0305
# pylint: disable=R0904


import unittest

import socialnetwork_model as sn

from collections.abc import Iterable


class TestSN(unittest.TestCase):
    '''
    Class definition for unit tests for main.py
    '''

    def setUp(self):
        '''
        Test initialization of the users and todo collections
        '''
        self.user_col = sn.UserCollection()
        self.assertIsInstance(
            self.user_col,
            sn.UserCollection,
            msg="Returned object not user_collection"
        )

        self.todo_col = sn.ToDoCollection()
        self.assertIsInstance(
            self.todo_col,
            sn.ToDoCollection,
            msg="Returned object not todo_collection"
        )

    def test_add_user(self):
        new_user = self.user_col.add_user( "cajopa", "cajopa@uw.edu", "Carl", "Parker" )
        self.assertTrue( new_user )

    def test_search_user(self):
        self.user_col.add_user( "lrac", "lrac@yahoo.edu", "Carl", "Parker" )
        user = self.user_col.search_user( "lrac" )
        self.assertEqual( user.user_id, "lrac" )

    def test_search_user_not_found(self):
        user = self.user_col.search_user( "carlp-20220509" )
        self.assertNotIsInstance(
            user,
            #
            # CHECKCHECK: Correct type below?
            #
            sn.UsersTable
        )

    def test_mod_user(self):
        add_success = self.user_col.add_user( "spiderman", "peterpa@uw.edu", "Carl", "Parker" )
        self.assertTrue( add_success )
        mod_success = self.user_col.modify_user( "spiderman", "peterpa@uw.edu", "Peter", "Parker" ) 
        self.assertTrue( mod_success )
        find_mod_user = self.user_col.search_user( "spiderman" )
        self.assertEqual( find_mod_user.user_name, "Peter" )

    def test_delete_user(self):
        add_success = self.user_col.add_user( "batman", "brucew@uw.edu", "Bruce", "Wayne" ) 
        self.assertTrue( add_success )
        del_success = self.user_col.delete_user( "batman" )
        self.assertTrue( del_success )


    def test_add_todo(self):
        self.user_col.add_user( "capra", "capra@uw.edu", "Eddie", "Bosco" )
        new_todo = self.todo_col.add_todo( "capra", "capra_0007", "HBO Max ads...:-P" )
        self.assertTrue( new_todo )

    def test_search_todo(self):
        self.user_col.add_user( "bmeau", "bmeau@uw.edu", "Bart", "Muller" )
        new_todo = self.todo_col.add_todo( "bmeau", "bmeau_0008", "Netflix ads as well" )
        self.assertTrue( new_todo )
        todo = self.todo_col.search_todo( "bmeau_0008" )
        self.assertEqual( todo.todo_text, "Netflix ads as well" )

    def test_modify_todo(self):
        self.user_col.add_user( "pfram", "pfram@uw.edu", "Peter", "Frampton" )
        new_todo = self.todo_col.add_todo( "pfram", "pfram_0001", "I prefer Disney" )
        self.assertTrue( new_todo )
        mod_success = self.todo_col.modify_todo( "pfram_0001", "pfram", "I heart Disney" )
        self.assertTrue( mod_success )

    def test_delete_todo(self):
        self.user_col.add_user( "jimmypage", "jimmyp@uw.edu", "Jimmy", "Page" )
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
        self.user_col.add_user( "maddrox", "maddrox@uw.edu", "Bart", "Muller" )
        new_todo = self.todo_col.add_todo( "maddrox", "maddrox_0008", "Netflix ads as well" )
        self.assertTrue( new_todo )
        new_todo = self.todo_col.add_todo( "maddrox", "maddrox_0009", "Amazon Prime has no ads" )
        self.assertTrue( new_todo )
        todo_list = self.todo_col.search_all_todo_updates( "maddrox" )
        self.assertIsInstance( todo_list, list )

    def test_filter_todo_by_string(self):
        self.user_col.add_user( "lukec", "lukec@uw.edu", "Luke", "Cage" )
        new_todo = self.todo_col.add_todo( "lukec", "lukec_0008", "Netflix hosts my show" )
        self.assertTrue( new_todo )
        new_todo = self.todo_col.add_todo( "lukec", "lukec_0009", "Amazon Prime is too lame to host my show" )
        self.assertTrue( new_todo )
        todo_iterator = self.todo_col.filter_todo_by_string( "host" )
        self.assertIsInstance( todo_iterator, Iterable )
        self.assertEquals( len( [ stat.todo_text for stat in todo_iterator ] ), 2 )


# --- END --- #

