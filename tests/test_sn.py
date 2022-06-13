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
        Test initialization of the users and status collections
        '''
        self.user_col = sn.UserCollection()
        self.assertIsInstance(
            self.user_col,
            sn.UserCollection,
            msg="Returned object not user_collection"
        )

        self.status_col = sn.UserStatusCollection()
        self.assertIsInstance(
            self.status_col,
            sn.UserStatusCollection,
            msg="Returned object not status_collection"
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


    def test_add_status(self):
        self.user_col.add_user( "capra", "capra@uw.edu", "Eddie", "Bosco" )
        new_status = self.status_col.add_status( "capra", "capra_0007", "HBO Max ads...:-P" )
        self.assertTrue( new_status )

    def test_search_status(self):
        self.user_col.add_user( "bmeau", "bmeau@uw.edu", "Bart", "Muller" )
        new_status = self.status_col.add_status( "bmeau", "bmeau_0008", "Netflix ads as well" )
        self.assertTrue( new_status )
        status = self.status_col.search_status( "bmeau_0008" )
        self.assertEqual( status.status_text, "Netflix ads as well" )

    def test_modify_status(self):
        self.user_col.add_user( "pfram", "pfram@uw.edu", "Peter", "Frampton" )
        new_status = self.status_col.add_status( "pfram", "pfram_0001", "I prefer Disney" )
        self.assertTrue( new_status )
        mod_success = self.status_col.modify_status( "pfram_0001", "pfram", "I heart Disney" )
        self.assertTrue( mod_success )

    def test_delete_status(self):
        self.user_col.add_user( "jimmypage", "jimmyp@uw.edu", "Jimmy", "Page" )
        new_status = self.status_col.add_status( "jimmypage", "jimmypage_0002", "BBC for me" )
        self.assertTrue( new_status )
        del_success = self.status_col.delete_status( "jimmypage_0002" )
        self.assertTrue( del_success )
        #
        # See if we can find the status we deleted
        #
        status = self.status_col.search_status( "jimmypage_0002" )
        self.assertIsNone( status )

    def test_delete_status_cascade(self):
        self.user_col.add_user( "rogerd", "rogerd@uw.edu", "Roger", "Daltry" )
        new_status = self.status_col.add_status( "rogerd", "rogerd_0009", "Can you see the real me?" )
        self.assertTrue( new_status )
        del_success = self.user_col.delete_user( "rogerd" )
        self.assertTrue( del_success )
        #
        # See if we can find the status we deleted.
        #
        # Should have been recursively deleted.
        #
        status = self.status_col.search_status( "rogerd_0009" )
        self.assertIsNone( status )

    def test_search_all_status_updates(self):
        self.user_col.add_user( "maddrox", "maddrox@uw.edu", "Bart", "Muller" )
        new_status = self.status_col.add_status( "maddrox", "maddrox_0008", "Netflix ads as well" )
        self.assertTrue( new_status )
        new_status = self.status_col.add_status( "maddrox", "maddrox_0009", "Amazon Prime has no ads" )
        self.assertTrue( new_status )
        status_list = self.status_col.search_all_status_updates( "maddrox" )
        self.assertIsInstance( status_list, list )

    def test_filter_status_by_string(self):
        self.user_col.add_user( "lukec", "lukec@uw.edu", "Luke", "Cage" )
        new_status = self.status_col.add_status( "lukec", "lukec_0008", "Netflix hosts my show" )
        self.assertTrue( new_status )
        new_status = self.status_col.add_status( "lukec", "lukec_0009", "Amazon Prime is too lame to host my show" )
        self.assertTrue( new_status )
        status_iterator = self.status_col.filter_status_by_string( "host" )
        self.assertIsInstance( status_iterator, Iterable )
        self.assertEquals( len( [ stat.status_text for stat in status_iterator ] ), 2 )


# --- END --- #

