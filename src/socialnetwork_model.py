'''
Provide an SQL infrastructure for social network
'''

import sys
import typing  # type: ignore  # noqa:F401  pylint:disable=unused-import

import peewee as pw  # type: ignore
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

db = pw.SqliteDatabase('sn.db')


class BaseModel( pw.Model ):
    '''
    Inherited by our other database classes.
    '''
    class Meta:
        '''
        Class composed into the BaseModel; evidently
        part of the pattern for peewee.
        '''
        database = db


class UsersTable( BaseModel ):
    '''
    Class for the users table in our database.
    Instances of this class correspond to rows in the table,
    where a row is an individual user.
    '''
    user_id = pw.CharField( primary_key = True,
                            max_length = 30,
                            constraints=[pw.Check("LENGTH(user_id) < 30")])
    user_name = pw.CharField( max_length = 30,
                              constraints=[pw.Check("LENGTH(user_name) < 30")])
    user_last_name = pw.CharField( max_length = 100,
                                   constraints=[
                                       pw.Check("LENGTH(user_last_name) < 100")
                                   ] )
    email = pw.CharField( max_length = 50,
                          constraints=[pw.Check("LENGTH(email) < 50")] )

    def show( self ):
        '''
        Prints the state of an instance of a user.
        '''
        print( self.user_id )
        print( self.user_name )
        print( self.user_last_name )
        print( self.email )


class ToDoTable( BaseModel ):
    '''
    Class for the ToDo table in our database.
    Instances of this class correspond to rows in the table,
    where a row is an individual ToDo item.
    '''
    todo_id = pw.CharField( max_length = 30,
                              constraints=[
                                  pw.Check("LENGTH(todo_id) < 30")
                              ]
                              )
    user_id = pw.ForeignKeyField( UsersTable,
                                  backref='posted_by',
                                  null = False
                                  )
    todo_text = pw.CharField( max_length = 128,
                                constraints=[
                                    pw.Check("LENGTH(todo_text) < 128")
                                ]
                                )


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

        if self.search_user( new_user_id ):
            logger.debug( "User already in database" )
            return False

        try:
            with db.transaction():
                new_user = UsersTable.create(
                    user_id = new_user_id,
                    user_name = new_user_name,
                    user_last_name = new_user_last_name,
                    email = new_email
                )
                new_user.save()
        except ( pw.DatabaseError,
                 pw.IntegrityError,
                 pw.NotSupportedError ) as db_exception:
            logger.info(f'Error creating user = {new_user_id}')
            logger.info(db_exception)
            return False

        else:
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
            with db.transaction():
                UsersTable.update(
                    user_name = mod_user_name,
                    user_last_name = mod_user_last_name,
                    email = mod_email
                ).where( UsersTable.user_id == mod_user_id ).execute()

            logger.debug( "user_to_mod.user_name: ", user_to_mod.user_name )

        except ( pw.DatabaseError,
                 pw.IntegrityError,
                 pw.NotSupportedError ) as db_exception:
            logger.info(f'Error modifying user = {mod_user_id}')
            logger.info(db_exception)

        logger.debug( "User updated" )
        return True

    def delete_user( self, delete_user_id ):
        '''
        Deletes a user from user_collection.

        Requirements:
        - Returns False if there are any errors (such as user_id not found)
        - Otherwise, it returns True.
        '''
        logger.debug( "Entering function" )

        user_to_del = self.search_user( delete_user_id )

        if user_to_del is None:
            logger.debug( "User not in database" )
            return False

        try:
            with db.transaction():
                user_to_del.delete_instance(
                    #
                    # Ensure that we delete any dependent rows
                    #
                    recursive = True
                )

            logger.debug( "user_to_del.user_name: ", user_to_del.user_name )

        except ( pw.DatabaseError,
                 pw.IntegrityError,
                 pw.NotSupportedError ) as db_exception:
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
            user = UsersTable.get_or_none( UsersTable.user_id == user_id )

        except ( pw.DatabaseError,
                 pw.IntegrityError,
                 pw.NotSupportedError ) as db_exception:
            logger.info(f'Error searching for user = {user_id}')
            logger.info(db_exception)

        else:
            if user:
                logger.debug( "User ID found" )
                logger.debug( "User type: ", type( user ) )
                return user
            logger.debug( "User ID not in database" )
            return None


class UserStatusCollection():
    '''
    Class to organize methods that operate on statuses.
    '''

    def __init__(self):
        logger.debug( "Initialize UserStatusCollection" )

    def add_status( self, new_status_user_id, new_todo_id, new_todo_text ):
        '''
        add a new status message to the collection
        '''
        logger.debug( "Entering method" )
        logger.debug( "Param: new_todo_id: " + new_todo_id )

        if self.search_status( new_todo_id ):
            logger.debug( "Status already in database" )
            return False

        try:
            with db.transaction():
                new_status = ToDoTable.create(
                    todo_id = new_todo_id,
                    user_id = new_status_user_id,
                    todo_text = new_todo_text,
                )
                new_status.save()

        except ( pw.DatabaseError,
                 pw.IntegrityError,
                 pw.NotSupportedError ) as db_exception:
            logger.info(f'Error creating status = {new_todo_id}')
            logger.info(db_exception)
            return False

        else:
            logger.debug( "Status added" )
            return True

    def modify_status( self, mod_todo_id, user_id, mod_todo_text ):
        '''
        Modifies an existing status
        '''
        logger.debug( "Entering method" )
        logger.debug( "Param: mod_todo_id: " + mod_todo_id )
        logger.debug( "Param: mod_todo_text: " + mod_todo_text )

        status_to_mod = self.search_status( mod_todo_id )

        if status_to_mod is None:
            logger.debug( "Status not in database" )
            return False

        try:
            with db.transaction():
                ToDoTable.update(
                    todo_text = mod_todo_text).where(
                        ( ToDoTable.todo_id == mod_todo_id)
                    and ( ToDoTable.user_id == user_id ) ).execute()  # noqa: E501 W503

            logger.debug(
                "status_to_mod.todo_text: ", status_to_mod.todo_text
            )

        except ( pw.DatabaseError,
                 pw.IntegrityError,
                 pw.NotSupportedError ) as db_exception:
            logger.info(f'Error modifying status = {mod_todo_id}')
            logger.info(db_exception)

        logger.debug( "User updated" )
        return True

    def delete_status( self, delete_todo_id ):
        '''
        Deletes a status from status_collection.

        Requirements:
        - Returns False if there are any errors (such as todo_id not found)
        - Otherwise, it returns True.
        '''
        logger.debug( "Entering function" )

        status_to_del = self.search_status( delete_todo_id )

        if status_to_del is None:
            logger.debug( "Status not in database" )
            return False

        try:
            with db.transaction():
                status_to_del.delete_instance(
                    #
                    # Ensure that we delete any dependent rows
                    #
                    recursive = True
                )

            logger.debug(
                "status_to_del.todo_text: ", status_to_del.todo_text
            )

        except ( pw.DatabaseError,
                 pw.IntegrityError,
                 pw.NotSupportedError ) as db_exception:
            logger.info(f'Error deleting status = {delete_todo_id}')
            logger.info(db_exception)
            return False

        else:
            logger.debug( "Status deleted" )
            return True

    def search_status( self, todo_id ):
        '''
        Searches for status data
        '''
        logger.debug( "Entering method" )
        logger.debug( "Param: todo_id: " + todo_id )

        try:
            status = ToDoTable.get_or_none(
                ToDoTable.todo_id == todo_id )

        except ( pw.DatabaseError,
                 pw.IntegrityError,
                 pw.NotSupportedError ) as db_exception:
            logger.info(f'Error searching for status = {todo_id}')
            logger.info(db_exception)

        else:
            if status:
                logger.debug( "Status ID found" )
                return status
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
            status_list = ToDoTable.select().where(
                ToDoTable.user_id == user_id )

        except ( pw.DatabaseError,
                 pw.IntegrityError,
                 pw.NotSupportedError ) as db_exception:
            logger.info(f'Error searching for statuses for {user_id}')
            logger.info(db_exception)

        else:
            if status_list:
                logger.debug( "Statuses for " + user_id + " found" )
                # pylint: disable=not-an-iterable
                return [ status.todo_text for status in status_list ]
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
            status_iterator = ToDoTable.select() \
                .where( ToDoTable.todo_text.contains( target_string )) \
                .iterator()

        except ( pw.DatabaseError,
                 pw.IntegrityError,
                 pw.NotSupportedError ) as db_exception:
            logger.info(f'Error searching for statuses {target_string}')
            logger.info(db_exception)

        else:
            if status_iterator:
                logger.debug( "Iterator for " + target_string + " retrieved" )
                return status_iterator
            logger.debug( "Could not retrieve iterator for {target_string}" )
            return None


#
# Set up database
#
logger.debug( "Connect to database" )
db.connect()

logger.debug( "Configure database" )
db.execute_sql( 'PRAGMA foreign_keys = ON;' )

logger.debug( "Create tables" )
db.create_tables(
    [
        UsersTable,
        ToDoTable
    ]
)

logger.debug( "Complete database setup" )


# --- END --- #

