'''
Classes for user information for the social network project
'''
# pylint: disable=R0903

from loguru import logger

import peewee as pw


class Users():
    '''
    Contains user information
    '''

    def __init__(self, user_id, email, user_name, user_last_name):
        logger.debug( "Entering method" )
        self.user_id = user_id
        self.email = email
        self.user_name = user_name
        self.user_last_name = user_last_name


class UserCollection():
    '''
    Contains a collection of Users objects
    '''

    def __init__(self):
        logger.debug( "Entering method" )
        self.database = {}

    def add_user(self, user_id, email, user_name, user_last_name):
        '''
        Adds a new user to the collection
        '''
        logger.debug( "Entering method" )
        if user_id in self.database:
            # Rejects new status if status_id already exists
            logger.error( "User ID already in database" )
            return False
        new_user = Users(user_id, email, user_name, user_last_name)
        self.database[user_id] = new_user
        logger.debug( "User added" )
        return True

    def modify_user(self, user_id, email, user_name, user_last_name):
        '''
        Modifies an existing user
        '''
        logger.debug( "Entering method" )
        if user_id not in self.database:
            logger.error( "User ID not in database" )
            return False
        self.database[user_id].email = email
        self.database[user_id].user_name = user_name
        self.database[user_id].user_last_name = user_last_name
        logger.debug( "User deleted" )
        return True

    def delete_user(self, user_id):
        '''
        Deletes an existing user
        '''
        logger.debug( "Entering method" )
        if user_id not in self.database:
            logger.error( "User ID not in database" )
            return False
        del self.database[user_id]
        logger.debug( "User deleted" )
        return True

    def search_user(self, user_id):
        '''
        Searches for user data
        '''
        logger.debug( "Entering method" )
        logger.debug( "Param: user_id: " + user_id )
        if user_id not in self.database:
            logger.debug( "User ID not in database" )
            return Users(None, None, None, None)
        logger.debug( "User ID found" )
        return self.database[user_id]
