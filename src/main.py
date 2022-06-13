'''
main driver for a simple social network project
'''

#
# Unusused imports
#
# pylint: disable=W0611

import sys
import csv

#
# When specifying both flake8 and pylint directives
# on the same line, flake8 needs to come first.
# Otherwise, pylint will become confused.
#
import pysnooper  # noqa:F401  type: ignore  pylint:disable=unused-import
from loguru import logger

import socialnetwork_model as sn

logger.remove()

LOG_FORMAT = "{time:YYYY-MM-DD @ HH:mm:ss} | {level} | " + \
             "{file} : {function} : {line} : {message}"

logger.add( sys.stderr,
            format=LOG_FORMAT,
            level="DEBUG" )

logger.add( "log_{time:YYYY-MM-DD}.log",
            format=LOG_FORMAT,
            level="DEBUG" )

def init_user_collection():
    '''
    Creates and returns a new instance of UserCollection
    '''
    logger.debug( "Entering function" )
    user_col = sn.UserCollection()
    return user_col


def init_status_collection():
    '''
    Creates and returns a new instance of UserStatusCollection
    '''
    logger.debug( "Entering function" )
    status_col = sn.UserStatusCollection()
    return status_col


def load_users(filename, user_collection):
    '''
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    '''
    logger.debug( "Entering function" )
    logger.debug( "Param: filename: " + filename )
    logger.debug( "Param: user_collection: " + str( type( user_collection ) ) )

    with open(filename, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        #
        # USER_ID, EMAIL, NAME, LASTNAME
        #
        for row in reader:
            if search_user( row['USER_ID'], user_collection ) is None:
                #
                # Check for missing attributes
                #
                for user_attr in row.values():
                    if not user_attr:
                        return False
                user_collection.add_user(
                    row['USER_ID'],
                    row['EMAIL'],
                    row['NAME'],
                    row['LASTNAME']
                )
            else:
                continue
    return True


def save_users(filename, user_collection):  # pylint:disable=unused-argument
    '''
    This function is now a stub
    '''
    logger.debug( "Entering function" )
    logger.debug( "This function is now stub" )
    return True


def load_status_updates(filename, status_collection):
    '''
    Opens a CSV file with status data and adds it to an existing
    instance of UserStatusCollection

    Requirements:
    - If a status_id already exists, it will ignore it and continue to
      the next.
    - Returns False if there are any errors(such as empty fields in the
      source CSV file)
    - Otherwise, it returns True.
    '''
    logger.debug( "Entering function" )
    with open(filename, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        #
        # STATUS_ID, USER_ID, STATUS_TEXT
        #
        for row in reader:
            if search_status( row['STATUS_ID'], status_collection ) is None:
                #
                # Check for missing attributes
                #
                for status_attr in row.values():
                    if not status_attr:
                        return False
                status_collection.add_status(
                    row['USER_ID'],
                    row['STATUS_ID'],
                    row['STATUS_TEXT']
                )
            else:
                continue
    return True


def save_status_updates(filename, status_collection):  # pylint:disable=unused-argument
    '''
    This function is now a stub
    '''
    logger.debug( "Entering function" )
    logger.debug( "This function is now stub" )
    return True


def add_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_user() returns False).
    - Otherwise, it returns True.
    '''
    logger.debug( "Entering function" )
    if search_user( user_id, user_collection ) is None:
        return user_collection.add_user(
            user_id,
            email,
            user_name,
            user_last_name
        )
    logger.error( "User already in database" )
    return False


def update_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    logger.debug( "Entering function" )
    if search_user( user_id, user_collection ) is not None:
        user_collection.modify_user(
            user_id,
            email,
            user_name,
            user_last_name
        )
        return True
    #
    # A user with that ID doesn't exist, so cannot update
    #
    logger.error( "No user found with that ID" )
    return False


def delete_user(user_id, user_collection):
    '''
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    logger.debug( "Entering function" )
    user_to_delete = search_user( user_id, user_collection )
    if user_to_delete is None:
        logger.error( "No user found with that ID" )
        return False
    user_collection.delete_user( user_id )
    return True


def search_user(user_id, user_collection):
    '''
    Searches for a user in user_collection(which is an instance of
    UserCollection).

    Requirements:
    - If the user is found, returns the corresponding User instance.
    - Otherwise, it returns None.
    '''
    logger.debug( "Entering function" )
    logger.debug( "Param: user_id: " + user_id )
    logger.debug( "Param: user_collection: " + str( type( user_collection ) ) )
    search_result = user_collection.search_user(user_id)
    if search_result is None:
        logger.debug( "Could not find user in database" )
        return None
    logger.debug( "User found: " + search_result.user_id )
    logger.debug( "Type found: " + str( type( search_result ) ) )
    return search_result


def add_status(user_id, status_id, status_text, status_collection):
    '''
    Creates a new instance of UserStatus and stores it in
    user_collection(which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_status() returns False).
    - Otherwise, it returns True.
    '''
    logger.debug( "Entering function" )
    if search_status( status_id, status_collection ) is None:
        return status_collection.add_status( user_id, status_id, status_text )
    return False


def update_status(status_id, user_id, status_text, status_collection):
    '''
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    logger.debug( "Entering function" )
    if search_status( status_id, status_collection ) is not None:
        status_collection.modify_status( status_id, user_id, status_text )
        return True
    #
    # A status with that ID doesn't exist, so cannot update
    #
    return False


def delete_status(status_id, status_collection):
    '''
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    '''
    logger.debug( "Entering function" )
    status_to_delete = search_status( status_id, status_collection )
    if status_to_delete is None:
        return False
    status_collection.delete_status( status_id )
    return True


def search_status(status_id, status_collection):
    '''
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    '''
    logger.debug( "Entering function" )
    search_result = status_collection.search_status(status_id)
    if search_result is None:
        return None
    return search_result


def search_all_status_updates( user_id, status_collection ):
    '''
    Returns all the status updates for a specified user.

    Requirements:
    - If the user is found, returns the corresponding
    UserStatus instances as a list.
    - Otherwise, it returns None.
    '''
    logger.debug( "Entering function" )
    search_result = status_collection.search_all_status_updates( user_id )
    if search_result is None:
        return None
    return search_result


def filter_status_by_string( target_string, status_collection ):
    '''
    Returns all the status updates for a specified user.

    Requirements:
    - Returns an iterator to all status updates that contain the
      specified string. Note that there might not be any such status
      updates . . . :-O
    '''
    logger.debug( "Entering method" )
    logger.debug( "Param: target_string: " + target_string )

    status_iterator = status_collection.filter_status_by_string( target_string )
    if status_iterator is None:
        return None
    return status_iterator


# --- END --- #

