'''
classes to manage the user status messages
'''
# pylint: disable=R0903

from loguru import logger

import peewee as pw


class UserStatus():
    '''
    class to hold status message data
    '''

    def __init__(self, status_id, user_id, status_text):
        logger.debug( "Entering method" )
        self.status_id = status_id
        self.user_id = user_id
        self.status_text = status_text


class UserStatusCollection():
    '''
    Collection of UserStatus messages
    '''

    def __init__(self):
        logger.debug( "Entering method" )
        self.database = {}

    def add_status(self, status_id, user_id, status_text):
        '''
        add a new status message to the collection
        '''
        logger.debug( "Entering method" )
        if status_id in self.database:
            # Rejects new status if status_id already exists
            logger.error( "Status ID already exists" )
            return False
        new_status = UserStatus(status_id, user_id, status_text)
        self.database[status_id] = new_status
        logger.debug( "Status added" )
        return True

    def modify_status(self, status_id, user_id, status_text):
        '''
        Modifies a status message

        The new user_id and status_text are assigned to the existing message
        '''
        logger.debug( "Entering method" )
        if status_id not in self.database:
            # Rejects update is the status_id does not exist
            logger.error( "Status ID does not exists" )
            return False
        self.database[status_id].user_id = user_id
        self.database[status_id].status_text = status_text
        logger.debug( "Status modified" )
        return True

    def delete_status(self, status_id):
        '''
        deletes the status message with id, status_id
        '''
        logger.debug( "Entering method" )
        if status_id not in self.database:
            # Fails if status does not exist
            logger.error( "Status ID does not exists" )
            return False
        del self.database[status_id]
        logger.debug( "Status deleted" )
        return True

    def search_status(self, status_id):
        '''
        Find and return a status message by its status_id

        Returns an empty UserStatus object if status_id does not exist
        '''
        logger.debug( "Entering method" )
        if status_id not in self.database:
            # Fails if the status does not exist
            logger.debug( "Status ID does not exists" )
            return UserStatus(None, None, None)
        logger.debug( "Status found" )
        return self.database[status_id]
