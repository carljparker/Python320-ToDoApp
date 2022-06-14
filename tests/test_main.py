'''
Unit test module for functions in main.py
'''

# pylint: disable=C0305
# pylint: disable=R0904

from collections.abc import Iterable

import unittest

import socialnetwork_model as sn

import main as main


class TestMain(unittest.TestCase):
    '''
    Class definition for unit tests for main.py
    '''
    def test_init_user_collection(self):
        '''
        Test initialization of the collection of users
        '''
        user_col = main.init_user_collection()
        self.assertIsInstance(
            user_col,
            sn.UserCollection,
            msg="Returned object not UserCollection"
        )

    def test_init_todo_collection(self):
        '''
        Test initialization of the collection of todos
        '''
        todo_col = main.init_todo_collection()
        self.assertIsInstance(
            todo_col,
            sn.ToDoCollection,
            msg="Returned object not ToDoCollection"
        )

    def test_1_load_users(self):
        '''
        Test loading users from a CSV into the collection
        '''
        user_col = main.init_user_collection()
        self.assertIs( main.load_users( "accounts.csv", user_col ), True )

    def test_save_users(self):
        '''
        Test saving users from the collection to a CSV
        '''
        user_col = main.init_user_collection()
        main.load_users( "accounts.csv", user_col )
        self.assertIs( main.save_users( "accounts-new.csv", user_col), True )

    def test_load_bad_users(self):
        '''
        Test how we handle loading a malformed CSV of users
        '''
        user_col = main.init_user_collection()
        self.assertIs( main.load_users( "accounts-bad.csv", user_col ), False)

    def test_2_load_todo_updates(self):
        '''
        Test loading todos from a CSV into the collection
        '''
        todo_col = main.init_todo_collection()
        self.assertIs(
            main.load_todo_updates(
                "status_updates_reasonable.csv",
                todo_col
            ),
            True
        )


    def test_load_bad_todo_updates(self):
        '''
        Test how we handle loading a malformed CSV of todos
        '''
        todo_col = main.init_todo_collection()
        self.assertIs(
            main.load_todo_updates(
                "status_updates_bad.csv",
                todo_col
            ),
            False
        )

    def test_add_user(self):
        '''
        Test whether we can add a user
        '''
        user_col = main.init_user_collection()
        self.assertIs( main.load_users( "accounts.csv", user_col ), True )
        self.assertIs(
            main.add_user(
                "cajopa",
                "carljparker@gmail.com",
                "Carl",
                "Parker",
                user_col
            ),
            True
        )

    def test_add_user_fail(self):
        '''
        Test how we handle trying to add a malformed user
        '''
        user_col = main.init_user_collection()
        self.assertIs( main.load_users( "accounts.csv", user_col ), True )
        self.assertIs(
            main.add_user(
                "evmiles97",
                "eve.miles@uw.edu",
                "Eve",
                "Miles",
                user_col
            ),
            True
        )
        #
        # Add same user a second time
        #
        self.assertIsNot(
            main.add_user(
                "evmiles97",
                "eve.miles@uw.edu",
                "Eve",
                "Miles",
                user_col
            ),
            True
        )

    def test_update_user(self):
        '''
        Test whether we can update the data for a user
        '''
        user_col = main.init_user_collection()
        self.assertIs( main.load_users( "accounts.csv", user_col ), True )
        self.assertIs(
            #
            # Ms Miles got married and changed her last name
            #
            main.update_user(
                "evmiles97",
                "eve.miles@uw.edu",
                "Eve",
                "Kilos",
                user_col
            ),
            True
        )
        return True

    def test_update_user_fail(self):
        '''
        Test whether the code to add a user fails appropriately
        '''
        user_col = main.init_user_collection()
        self.assertIs( main.load_users( "accounts.csv", user_col ), True )
        self.assertIsNot(
            #
            # Ms Miles got married and changed her last name
            #
            main.update_user(
                "evmiles9x",
                "eve.miles@uw.edu",
                "Eve",
                "Kilos",
                user_col
            ),
            True
        )
        return True

    def test_delete_user(self):
        '''
        Test whether we can delete a user from the collection
        '''
        user_col = main.init_user_collection()
        main.load_users( "accounts.csv", user_col )
        test_user_id = 'Isabel.Avivah34'
        self.assertIs( main.delete_user( test_user_id, user_col ), True )
        self.assertIs(
            main.save_users(
                "accounts-with-delete.csv",
                user_col
            ),
            True
        )

    def test_delete_user_fail(self):
        '''
        Test whether the code to delete a user fails when we expect it to
        '''
        user_col = main.init_user_collection()
        main.load_users( "accounts.csv", user_col )
        test_user_id = 'dave0x'
        self.assertIsNot( main.delete_user( test_user_id, user_col ), True )
        self.assertIs(
            main.save_users(
                "accounts-with-delete.csv",
                user_col
            ),
            True
        )

    def test_search_user(self):
        '''
        Test whether we can find a user that we know exists
        '''
        user_col = main.init_user_collection()
        main.load_users( "accounts.csv", user_col )
        test_user_id = 'dave03'
        self.assertIsInstance(
            main.search_user( test_user_id, user_col ),
            sn.UsersTable,
            msg = "Failed to find user"
        )

    def test_search_user_fail(self):
        '''
        Test whether we fail to find a user that we know does *not* exist
        '''
        user_col = main.init_user_collection()
        main.load_users( "accounts.csv", user_col )
        test_user_id = 'dave0x'
        self.assertNotIsInstance(
            main.search_user( test_user_id, user_col ),
            sn.UsersTable,
            msg = "Failed to find user"
        )

    def test_add_todo(self):
        '''
        Test whether we can add a todo to the collection
        '''
        todo_col = main.init_todo_collection()
        self.assertIs(
            main.load_todo_updates(
                "status_updates_reasonable.csv",
                todo_col
            ),
            True
        )
        user_col = main.init_user_collection()
        self.assertIs( main.load_users( "accounts.csv", user_col ), True )
        self.assertIs( main.add_user( "pfram", "pfram@yahoo.com", "Peter", "Frampton", user_col ), True )
        self.assertIs(
            main.add_todo(
                "pfram",
                "pfram_777",
                "I can has todo",
                todo_col
            ),
            True
        )

    def test_add_todo_fail(self):
        '''
        Test whether we fail to add a todo when we expect to fail
        '''
        todo_col = main.init_todo_collection()
        self.assertIs(
            main.load_todo_updates(
                "status_updates_reasonable.csv",
                todo_col
            ),
            True
        )
        self.assertIsNot(
            main.add_todo(
                "evmiles97",
                "evmiles97_00002",
                "Perfect weather for a hiking",
                todo_col
            ),
            True
        )

    def test_update_todo(self):
        '''
        Test whether we can update the data for a todo
        '''
        todo_col = main.init_todo_collection()
        self.assertIs(
            main.load_todo_updates(
                "status_updates_reasonable.csv",
                todo_col
            ),
            True
        )  
        self.assertIs(
            main.update_todo(
                "Isabel.Avivah34_27",
                "Isabel.Avivah34",
                "Perfect weather for a skiing",
                todo_col
            ),
            True
        )
        self.assertIs(
            main.save_todo_updates(
                "todo_updates-with-mod.csv",
                todo_col
            ),
            True
        )

    def test_update_todo_fail(self):
        '''
        Test whether trying to update a todo fails when we expect it to
        '''
        todo_col = main.init_todo_collection()
        self.assertIs(
            main.load_todo_updates(
                "status_updates_reasonable.csv",
                todo_col
            ),
            True
        )
        self.assertIsNot(
            main.update_todo(
                "cajopa_00001",
                "cajopa",
                "I can *have* todo",
                todo_col
            ),
            True
        )

    def test_delete_todo(self):
        '''
        Test whether we can delete a todo from the collection
        '''
        todo_col = main.init_todo_collection()
        main.load_todo_updates( "status_updates_reasonable.csv", todo_col )
        test_todo_id = 'Isabel.Avivah34_27'
        self.assertIs(
            main.delete_todo(
                test_todo_id,
                todo_col ),
            True
        )
        self.assertIs(
            main.save_todo_updates(
                "todo_updates-with-delete.csv",
                todo_col
            ),
            True
        )

    def test_delete_todo_fail(self):
        '''
        Test whether we fail to delete a todo when we expect it to fail
        '''
        todo_col = main.init_todo_collection()
        main.load_todo_updates( "status_updates_reasonable.csv", todo_col )
        test_todo_id = 'evmiles97_0000x'
        self.assertIsNot(
            main.delete_todo(
                test_todo_id, todo_col
            ),
            True
        )
        self.assertIs(
            main.save_todo_updates(
                "todo_updates-with-delete.csv",
                todo_col
            ),
            True
        )

    def test_search_todo(self):
        '''
        Test whether we can find a todo that we know is there
        '''
        user_col = main.init_user_collection()
        self.assertTrue( main.load_users( "accounts.csv", user_col ) )
        todo_col = main.init_todo_collection()
        todo_data = "status_updates_reasonable.csv"
        test_todo_id = 'Isabel.Avivah34_27'
        self.assertTrue( main.load_todo_updates( todo_data, todo_col ) )
        self.assertIsInstance(
            main.search_todo( test_todo_id, todo_col ),
            sn.ToDoTable,
            msg = "Failed to find todo [" + 
                  test_todo_id + 
                  "] in [" + 
                  todo_data +
                  "]" 
        )

    def test_search_all_todo_upates(self):
        '''
        Test whether we can find all the todo updates for a 
        user that we know has multiple updates.
        '''
        user_col = main.init_user_collection()
        self.assertTrue( main.load_users( "accounts.csv", user_col ) )
        todo_col = main.init_todo_collection()
        todo_data = "status_updates_reasonable.csv"
        self.assertTrue( main.load_todo_updates( todo_data, todo_col ) )
        test_user_id = 'Tonye.Nella57'
        list_of_todo = main.search_all_todo_updates( test_user_id,
                                                         todo_col )
        self.assertIsInstance(
            list_of_todo,
            list,
            msg = "main.search_all_todo_updates() did not return a list" )

    def test_search_all_todo_upates(self):
        '''
        Test whether we can find all the todo updates for a 
        user that we know has multiple updates.
        '''
        user_col = main.init_user_collection()
        self.assertTrue( main.load_users( "accounts.csv", user_col ) )
        todo_col = main.init_todo_collection()
        todo_data = "status_updates_reasonable.csv"
        self.assertTrue( main.load_todo_updates( todo_data, todo_col ) )
        test_target_text = 'zebra'
        todo_iterator = main.filter_todo_by_string( test_target_text,
                                                        todo_col )
        self.assertIsInstance(
            todo_iterator,
            Iterable,
            msg = "main.filter_todo_by_string did not return an iterator" )
        self.assertEquals( len( [ stat for stat in todo_iterator ] ), 3 )


    def test_search_todo_fail(self):
        '''
        Test whether we fail to find a todo that we know is not there
        '''
        todo_col = main.init_todo_collection()
        main.load_todo_updates( "status_updates_reasonable.csv", todo_col )
        test_todo_id = 'evmiles97_0000x'
        self.assertNotIsInstance(
            main.search_todo( test_todo_id, todo_col ),
            sn.ToDoTable,
            msg = "Failed to find todo"
        )


# --- END --- #

