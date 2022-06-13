'''
Unit test module for functions in main.py
'''

# pylint: disable=C0305
# pylint: disable=R0904

from collections.abc import Iterable

import unittest

import socialnetwork_model as sn

import main


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

    def test_init_status_collection(self):
        '''
        Test initialization of the collection of statuses
        '''
        status_col = main.init_status_collection()
        self.assertIsInstance(
            status_col,
            sn.UserStatusCollection,
            msg="Returned object not UserStatusCollection"
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

    def test_2_load_status_updates(self):
        '''
        Test loading statuses from a CSV into the collection
        '''
        status_col = main.init_status_collection()
        self.assertIs(
            main.load_status_updates(
                "status_updates_reasonable.csv",
                status_col
            ),
            True
        )


    def test_load_bad_status_updates(self):
        '''
        Test how we handle loading a malformed CSV of statuses
        '''
        status_col = main.init_status_collection()
        self.assertIs(
            main.load_status_updates(
                "status_updates_bad.csv",
                status_col
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

    def test_add_status(self):
        '''
        Test whether we can add a status to the collection
        '''
        status_col = main.init_status_collection()
        self.assertIs(
            main.load_status_updates(
                "status_updates_reasonable.csv",
                status_col
            ),
            True
        )
        user_col = main.init_user_collection()
        self.assertIs( main.load_users( "accounts.csv", user_col ), True )
        self.assertIs( main.add_user( "pfram", "pfram@yahoo.com", "Peter", "Frampton", user_col ), True )
        self.assertIs(
            main.add_status(
                "pfram",
                "pfram_777",
                "I can has status",
                status_col
            ),
            True
        )

    def test_add_status_fail(self):
        '''
        Test whether we fail to add a status when we expect to fail
        '''
        status_col = main.init_status_collection()
        self.assertIs(
            main.load_status_updates(
                "status_updates_reasonable.csv",
                status_col
            ),
            True
        )
        self.assertIsNot(
            main.add_status(
                "evmiles97",
                "evmiles97_00002",
                "Perfect weather for a hiking",
                status_col
            ),
            True
        )

    def test_update_status(self):
        '''
        Test whether we can update the data for a status
        '''
        status_col = main.init_status_collection()
        self.assertIs(
            main.load_status_updates(
                "status_updates_reasonable.csv",
                status_col
            ),
            True
        )  
        self.assertIs(
            main.update_status(
                "Isabel.Avivah34_27",
                "Isabel.Avivah34",
                "Perfect weather for a skiing",
                status_col
            ),
            True
        )
        self.assertIs(
            main.save_status_updates(
                "status_updates-with-mod.csv",
                status_col
            ),
            True
        )

    def test_update_status_fail(self):
        '''
        Test whether trying to update a status fails when we expect it to
        '''
        status_col = main.init_status_collection()
        self.assertIs(
            main.load_status_updates(
                "status_updates_reasonable.csv",
                status_col
            ),
            True
        )
        self.assertIsNot(
            main.update_status(
                "cajopa_00001",
                "cajopa",
                "I can *have* status",
                status_col
            ),
            True
        )

    def test_delete_status(self):
        '''
        Test whether we can delete a status from the collection
        '''
        status_col = main.init_status_collection()
        main.load_status_updates( "status_updates_reasonable.csv", status_col )
        test_status_id = 'Isabel.Avivah34_27'
        self.assertIs(
            main.delete_status(
                test_status_id,
                status_col ),
            True
        )
        self.assertIs(
            main.save_status_updates(
                "status_updates-with-delete.csv",
                status_col
            ),
            True
        )

    def test_delete_status_fail(self):
        '''
        Test whether we fail to delete a status when we expect it to fail
        '''
        status_col = main.init_status_collection()
        main.load_status_updates( "status_updates_reasonable.csv", status_col )
        test_status_id = 'evmiles97_0000x'
        self.assertIsNot(
            main.delete_status(
                test_status_id, status_col
            ),
            True
        )
        self.assertIs(
            main.save_status_updates(
                "status_updates-with-delete.csv",
                status_col
            ),
            True
        )

    def test_search_status(self):
        '''
        Test whether we can find a status that we know is there
        '''
        user_col = main.init_user_collection()
        self.assertTrue( main.load_users( "accounts.csv", user_col ) )
        status_col = main.init_status_collection()
        status_data = "status_updates_reasonable.csv"
        test_status_id = 'Isabel.Avivah34_27'
        self.assertTrue( main.load_status_updates( status_data, status_col ) )
        self.assertIsInstance(
            main.search_status( test_status_id, status_col ),
            sn.StatusTable,
            msg = "Failed to find status [" + 
                  test_status_id + 
                  "] in [" + 
                  status_data +
                  "]" 
        )

    def test_search_all_status_upates(self):
        '''
        Test whether we can find all the status updates for a 
        user that we know has multiple updates.
        '''
        user_col = main.init_user_collection()
        self.assertTrue( main.load_users( "accounts.csv", user_col ) )
        status_col = main.init_status_collection()
        status_data = "status_updates_reasonable.csv"
        self.assertTrue( main.load_status_updates( status_data, status_col ) )
        test_user_id = 'Tonye.Nella57'
        list_of_status = main.search_all_status_updates( test_user_id,
                                                         status_col )
        self.assertIsInstance(
            list_of_status,
            list,
            msg = "main.search_all_status_updates() did not return a list" )

    def test_search_all_status_upates(self):
        '''
        Test whether we can find all the status updates for a 
        user that we know has multiple updates.
        '''
        user_col = main.init_user_collection()
        self.assertTrue( main.load_users( "accounts.csv", user_col ) )
        status_col = main.init_status_collection()
        status_data = "status_updates_reasonable.csv"
        self.assertTrue( main.load_status_updates( status_data, status_col ) )
        test_target_text = 'zebra'
        status_iterator = main.filter_status_by_string( test_target_text,
                                                        status_col )
        self.assertIsInstance(
            status_iterator,
            Iterable,
            msg = "main.filter_status_by_string did not return an iterator" )
        self.assertEquals( len( [ stat for stat in status_iterator ] ), 3 )


    def test_search_status_fail(self):
        '''
        Test whether we fail to find a status that we know is not there
        '''
        status_col = main.init_status_collection()
        main.load_status_updates( "status_updates_reasonable.csv", status_col )
        test_status_id = 'evmiles97_0000x'
        self.assertNotIsInstance(
            main.search_status( test_status_id, status_col ),
            sn.StatusTable,
            msg = "Failed to find status"
        )


# --- END --- #

