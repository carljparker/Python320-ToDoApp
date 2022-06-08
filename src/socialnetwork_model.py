'''
Provide an SQL infrastructure for social network
'''

import sys
import typing  # type: ignore  # noqa:F401  pylint:disable=unused-import

from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from pymongo.errors import PyMongoError

#
# When specifying both flake8 and pylint directives
# on the same line, flake8 needs to come first.
# Otherwise, pylint will become confused.
#
import pysnooper  # type: ignore  # noqa:F401  pylint:disable=unused-import
from loguru import logger

#
# Logging config
#
logger.remove()

LOG_FORMAT = "{time:YYYY-MM-DD @ HH:mm:ss} | {level} | " + \
             "{file} : {function} : {line} : {message}"

logger.add( sys.stderr,
            format=LOG_FORMAT,
            level="DEBUG" )

logger.add( "log_{time:YYYY-MM-DD}.log",
            format=LOG_FORMAT,
            level="DEBUG" )

class UsersTable():
    '''
    Instances of this class correspond to rows in the table,
    where a row is an individual user.
    '''
    def __init__(self, user_id, user_name, user_last_name, email ):
        logger.debug( "UsersTable" )
        self.user_id   = user_id
        self.user_name = user_name
        self.user_last_name = user_last_name
        self.email     = email

    @staticmethod
    def as_dict( user_id, user_name, user_last_name, email ):
        '''
        Create a dictionary for a new user.
        '''
        logger.debug( "Entering method" )

        new_user = {}
        new_user[ 'user_id' ]   = user_id
        new_user[ 'user_name' ] = user_name
        new_user[ 'user_last_name' ] = user_last_name
        new_user[ 'email' ]     = email

        return new_user


class UserCache():
    cache = {}

    @classmethod
    def store( self, userID ):
        logger.debug( f"userID: {userID}" )
        if userID not in self.cache:
            self.cache[ userID ] = 1
            return True
        logger.warning( f"userID: {userID} already in cache" )
        return False

    @classmethod
    def read( self, userID ):
        logger.debug( f"userID: {userID}" )
        if userID in self.cache:
            return True
        logger.warning( f"userID: {userID} not in cache" )
        return False

    @classmethod
    def erase( self, userID ):
        logger.debug( f"userID: {userID}" )
        if userID in self.cache:
            del self.cache[ userID ]
            return True
        logger.warning( f"userID: {userID} not in cache" )
        return False


class StatusTable():
    '''
    Instances of this class correspond to rows in the table,
    where a row is an individual status.
    '''
    def __init__(self, status_id, user_id, status_text ):
        logger.debug( "StatusTable" )
        self.status_id   = status_id
        self.user_id     = user_id
        self.status_text = status_text

    @staticmethod
    def as_dict( status_id, user_id, status_text ):
        '''
        Create a dictionary object that conforms to the schema for a
        status
        '''
        logger.debug( "Entering method" )

        new_status = {}
        new_status[ 'status_id' ]   = status_id
        new_status[ 'user_id' ]   = user_id
        new_status[ 'status_text' ] = status_text

        return new_status

def dict_to_status_gen( dict_iterator ):
    '''
    Create a generator of StatusTable objects
    from an iterator of status dictionaries
    '''
    logger.debug( "Enter function" )

    for status_dict in dict_iterator:
        yield( StatusTable(
                status_dict[ "status_id" ],
                status_dict[ "user_id" ],
                status_dict[ "status_text" ]
            )
        )

class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


class UserCollection():
    '''
    Class to organize methods that operate on users.
    '''
    def __init__(self):
        logger.debug( "UserCollection" )

    def add_user( self, new_user_id, new_email,
                  new_user_name, new_user_last_name ):
        '''
        Adds a new user to the collection
        '''
        logger.debug( "Entering method" )
        logger.debug( "Param: user_id: " + new_user_id )

        if UserCache().read( new_user_id ):
            logger.debug( "User already in database" )
            return False

        try:
            with mongo:
                d_b = mongo.connection.media
                users_collection = d_b["users"]
                new_user = UsersTable.as_dict(
                    user_id = new_user_id,
                    user_name = new_user_name,
                    user_last_name = new_user_last_name,
                    email = new_email
                )
                users_collection.insert_one( new_user )

        except ( PyMongoError ) as db_exception:
            logger.info(f'Error creating user = {new_user_id}')
            logger.info(db_exception)
            return False

        else:
            UserCache().store( new_user_id )
            logger.debug( "User added" )
            return True

    def modify_user( self, mod_user_id, mod_email,
                     mod_user_name, mod_user_last_name):
        '''
        Modifies an existing user
        '''
        logger.debug( "Entering method" )
        logger.debug( "Param: mod_user_id: " + mod_user_id )
        logger.debug( "Param: mod_user_name: " + mod_user_name )

        user_to_mod = self.search_user( mod_user_id )

        if user_to_mod is None:
            logger.debug( "User not in database" )
            return False

        try:
            with mongo:
                d_b = mongo.connection.media
                users_collection = d_b["users"]

                query_json  = { 'user_id': mod_user_id }
                update_json = { '$set': {
                        'user_name': mod_user_name,
                        'user_last_name': mod_user_last_name,
                        'email': mod_email,
                    }
                }

                updated_user = users_collection.find_one_and_update(
                        query_json,
                        update_json,
                        return_document=ReturnDocument.AFTER
                )

        except ( PyMongoError ) as db_exception:
            logger.info(f'Error modifying user = {mod_user_id}')
            logger.info(db_exception)

        if updated_user[ "email" ] == mod_email:
            logger.debug( "User updated" )
            return True
        return False

    def delete_user( self, delete_user_id ):
        '''
        Deletes a user from user_collection.

        Requirements:
        - Returns False if there are any errors (such as user_id not found)
        - Otherwise, it returns True.
        '''
        logger.debug( "Entering function" )
        logger.debug( f"delete_user_id: {delete_user_id}" )

        user_to_del = UserCache().read( delete_user_id )

        if not user_to_del:
            logger.debug( "User not in database" )
            return False
        logger.debug( f"delete_user_id: {delete_user_id}" )

        try:
            with mongo:
                d_b = mongo.connection.media
                users_collection = d_b["users"]

                query = { 'user_id': delete_user_id }
                users_collection.delete_one( query )

                #
                # Remove any statuses associated with this user
                #
                UserStatusCollection().delete_status_by_user( delete_user_id )

        except ( PyMongoError ) as db_exception:
            logger.info(f'Error modifying user = {delete_user_id}')
            logger.info(db_exception)
            return False

        else:
            logger.debug( "User deleted" )
            return True

    def search_user( self, user_id ):
        '''
        Searches for user data
        '''
        logger.debug( "Entering method" )
        logger.debug( "Param: user_id: " + user_id )


        try:
            with mongo:
                d_b = mongo.connection.media
                users_collection = d_b["users"]
                query = { 'user_id': user_id }
                user = users_collection.find_one( query )

        except ( PyMongoError ) as db_exception:
            logger.info(f'Error searching for user = {user_id}')
            logger.info(db_exception)

        else:
            if user:
                logger.debug( "User ID found" )
                logger.debug( f"User type: { type( user ) }" )
                return UsersTable( user["user_id"], user["user_name"],
                                   user["user_last_name"], user["email"] )
            logger.debug( "User ID not in database" )
            return None

class UserStatusCollection():
    '''
    Class to organize methods that operate on statuses.
    '''

    def __init__(self):
        logger.debug( "Initialize UserStatusCollection" )

    def add_status( self, new_status_user_id, new_status_id, new_status_text ):
        '''
        add a new status message to the collection
        '''
        logger.debug( "Entering method" )
        logger.debug( "Param: new_status_id: " + new_status_id )

        #
        # Before we add the status, need to verify that
        # the user is in the users table.
        #
        # (Normally handled by SQL constraints, but under
        # MongoDB need to do it ourselves.)
        #
        if UserCache().read( new_status_user_id ):
            logger.debug( f"Verified that {new_status_user_id} has an account" )
        else:
            logger.debug( f"No account found for {new_status_user_id}" )
            return False

        if self.search_status( new_status_id ):
            logger.debug( "Status already in database" )
            return False

        try:
            with mongo:
                d_b = mongo.connection.media
                status_collection = d_b["status"]
                new_status = StatusTable.as_dict(
                    status_id = new_status_id,
                    user_id = new_status_user_id,
                    status_text = new_status_text,
                )
                status_collection.insert_one( new_status )

        except ( PyMongoError ) as db_exception:
            logger.info(f'Error creating status = {new_status_id}')
            logger.info(db_exception)
            return False

        else:
            logger.debug( "Status added" )
            return True

    def modify_status( self, mod_status_id, user_id, mod_status_text ):
        '''
        Modifies an existing status
        '''
        # pylint:disable=unused-argument
        logger.debug( "Entering method" )
        logger.debug( "Param: mod_status_id: " + mod_status_id )
        logger.debug( "Param: mod_status_text: " + mod_status_text )

        status_to_mod = self.search_status( mod_status_id )

        if status_to_mod is None:
            logger.debug( "Status not in database" )
            return False

        try:
            with mongo:
                d_b = mongo.connection.media
                status_collection = d_b["status"]

                query_json  = { 'status_id': mod_status_id }
                update_json = { '$set': { 'status_text': mod_status_text } }

                updated_doc = status_collection.find_one_and_update(
                        query_json,
                        update_json,
                        return_document=ReturnDocument.AFTER
                )

        except ( PyMongoError ) as db_exception:
            logger.info(f'Error modifying status = {mod_status_id}')
            logger.info(db_exception)

        if updated_doc[ "status_text" ] == mod_status_text:
            logger.debug( "Status updated" )
            return True
        return False

    def delete_status( self, delete_status_id ):
        '''
        Deletes a status from status_collection.

        Requirements:
        - Returns False if there are any errors (such as status_id not found)
        - Otherwise, it returns True.
        '''
        logger.debug( "Entering function" )

        status_to_del = self.search_status( delete_status_id )

        if status_to_del is None:
            logger.debug( "Status not in database" )
            return False

        logger.debug(
            "status_to_del.status_text: ", status_to_del.status_text
        )

        try:
            with mongo:
                d_b = mongo.connection.media
                status_collection = d_b["status"]

                query = { 'status_id': delete_status_id }
                delete_result = status_collection.delete_one( query )
                logger.debug( f"{ delete_result.deleted_count } status deleted" )

        except ( PyMongoError ) as db_exception:
            logger.info(f'Error deleting status = {delete_status_id}')
            logger.info(db_exception)
            return False

        else:
            logger.debug( "Status deleted" )
            return True

    def delete_status_by_user( self, delete_user_id ):
        '''
        Deletes all statuses for the specified user from status_collection.

        Requirements:
        - Returns False if there are any errors (such as status_id not found)
        - Otherwise, it returns True.
        '''
        logger.debug( "Entering function" )

        try:
            with mongo:
                d_b = mongo.connection.media
                status_collection = d_b["status"]

                query = { 'user_id': delete_user_id }
                status_count = status_collection.count_documents( query )

                if status_count:
                    logger.debug(
                        f"Deleting { status_count } statuses "
                      + f"found for { delete_user_id }"
                    )
                else:
                    logger.debug( f"No statuses found for {delete_user_id}" )
                    return False

                status_collection.delete_many( query )

        except ( PyMongoError ) as db_exception:
            logger.info(f'Error deleting status for {delete_user_id}')
            logger.info(db_exception)
            return False

        else:
            logger.debug( "Status deleted" )
            return True

    def search_status( self, status_id ):
        '''
        Searches for status data
        '''
        logger.debug( "Entering method" )
        logger.debug( "Param: status_id: " + status_id )

        try:
            with mongo:
                d_b = mongo.connection.media
                status_collection = d_b["status"]
                query = { 'status_id': status_id }
                status = status_collection.find_one( query )

        except ( PyMongoError ) as db_exception:
            logger.info(f'Error searching for status = {status_id}')
            logger.info(db_exception)

        else:
            if status:
                logger.debug( "Status ID found" )
                return StatusTable(
                        status[ "status_id" ],
                        status[ "user_id" ],
                        status[ "status_text" ]
                )
            logger.debug( "Status ID not in database" )
            return None

    def search_all_status_updates( self, user_id ):
        '''
        Returns all the status updates for a specified user.

        Requirements:
        - If the user is found, returns the corresponding
          UserStatus instances as a list.
        - Otherwise, it returns None.
        '''
        logger.debug( "Entering method" )
        logger.debug( "Param: user_id: " + user_id )

        try:
            with mongo:
                d_b = mongo.connection.media
                status_collection = d_b["status"]
                query = { 'user_id': user_id }
                status_list = status_collection.find( query )

        except ( PyMongoError ) as db_exception:
            logger.info(f'Error searching for statuses for {user_id}')
            logger.info(db_exception)

        else:
            if status_list:
                logger.debug( "Statuses for " + user_id + " found" )
                # pylint: disable=not-an-iterable
                return [ status[ "status_text" ] for status in status_list ]
            logger.debug( "User ID: " + user_id + " not in database" )
            return None

    def filter_status_by_string( self, target_string: str ):
        '''
        Returns all the status updates for a specified user.

        Requirements:
        - Returns an iterator to all status updates that contain the
          specified string. Note that there might not be any such status
          updates . . . :-O
        '''
        logger.debug( "Entering method" )
        logger.debug( "Param: target_string: " + target_string )

        try:
            with mongo:
                d_b = mongo.connection.media
                status_collection = d_b["status"]
                #
                # https://stackoverflow.com/a/10616781/1106930
                #
                query = { 'status_text': { '$regex' : target_string } }
                status_iterator = status_collection.find( query )

        except ( PyMongoError ) as db_exception:
            logger.info(f'Error searching for statuses {target_string}')
            logger.info(db_exception)

        else:
            if status_iterator:
                logger.debug( "Iterator for " + target_string + " retrieved" )
                status_gen = dict_to_status_gen( status_iterator )
                return status_gen
            logger.debug( "Could not retrieve iterator for {target_string}" )
            return None


#
# Set up database
#
logger.debug( "Initialize context manager for MongoDB" )

mongo = MongoDBConnection()

logger.debug( "Complete database setup" )


# --- END --- #

