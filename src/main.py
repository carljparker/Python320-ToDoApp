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


def init_todo_collection():
    '''
    Creates and returns a new instance of ToDoCollection
    '''
    logger.debug( "Entering function" )
    todo_col = sn.ToDoCollection()
    return todo_col


def load_todo_updates(filename, todo_collection):
    '''
    Opens a CSV file with todo data and adds it to an existing
    instance of ToDoCollection

    Requirements:
    - If a todo_id already exists, it will ignore it and continue to
      the next.
    - Returns False if there are any errors(such as empty fields in the
      source CSV file)
    - Otherwise, it returns True.
    '''
    logger.debug( "Entering function" )
    with open(filename, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        #
        # TODO_ID, USER_ID, TODO_TEXT
        #
        for row in reader:
            if search_todo( row['STATUS_ID'], todo_collection ) is None:
                #
                # Check for missing attributes
                #
                for todo_attr in row.values():
                    if not todo_attr:
                        return False
                todo_collection.add_todo(
                    row['USER_ID'],
                    row['STATUS_ID'],
                    row['STATUS_TEXT']
                )
            else:
                continue
    return True


def save_todo_updates(filename, todo_collection):  # pylint:disable=unused-argument
    '''
    This function is now a stub
    '''
    logger.debug( "Entering function" )
    logger.debug( "This function is now stub" )
    return True


def add_todo(due_date, todo_id, todo_text, todo_collection):
    '''
    Creates a new instance of ToDo and stores it in
    user_collection(which is an instance of ToDoCollection)

    Requirements:
    - todo_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_todo() returns False).
    - Otherwise, it returns True.
    '''
    logger.debug( "Entering function" )
    if search_todo( todo_id, todo_collection ) is None:
        return todo_collection.add_todo( due_date, todo_id, todo_text )
    return False


def update_todo(todo_id, due_date, todo_text, todo_collection):
    '''
    Updates the values of an existing todo_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    logger.debug( "Entering function" )
    if search_todo( todo_id, todo_collection ) is not None:
        todo_collection.modify_todo( todo_id, due_date, todo_text )
        return True
    #
    # A todo with that ID doesn't exist, so cannot update
    #
    return False


def delete_todo(todo_id, todo_collection):
    '''
    Deletes a todo_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as todo_id not found)
    - Otherwise, it returns True.
    '''
    logger.debug( "Entering function" )
    todo_to_delete = search_todo( todo_id, todo_collection )
    if todo_to_delete is None:
        return False
    todo_collection.delete_todo( todo_id )
    return True


def search_todo(todo_id, todo_collection):
    '''
    Searches for a todo in todo_collection

    Requirements:
    - If the todo is found, returns the corresponding
    ToDo instance.
    - Otherwise, it returns None.
    '''
    logger.debug( "Entering function" )
    search_result = todo_collection.search_todo(todo_id)
    if search_result is None:
        return None
    return search_result


def search_all_todo_updates( due_date, todo_collection ):
    '''
    Returns all the todo updates for a specified user.

    Requirements:
    - If the user is found, returns the corresponding
      ToDo instances as a list.
    - Otherwise, it returns None.
    '''
    logger.debug( "Entering function" )
    search_result = todo_collection.search_all_todo_updates( due_date )
    if search_result is None:
        return None
    return search_result


def filter_todo_by_string( target_string, todo_collection ):
    '''
    Returns all the todo updates for a specified user.

    Requirements:
    - Returns an iterator to all todo updates that contain the
      specified string. Note that there might not be any such todo
      updates . . . :-O
    '''
    logger.debug( "Entering method" )
    logger.debug( "Param: target_string: " + target_string )

    todo_iterator = todo_collection.filter_todo_by_string( target_string )
    if todo_iterator is None:
        return None
    return todo_iterator


# --- END --- #

