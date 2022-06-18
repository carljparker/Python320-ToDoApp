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

db = pw.SqliteDatabase('td.db')


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
    due_date = pw.CharField( primary_key = True,
                            max_length = 30,
                            constraints=[pw.Check("LENGTH(due_date) < 30")])
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
        print( self.due_date )
        print( self.user_name )
        print( self.user_last_name )
        print( self.email )


class ToDoTable( BaseModel ):
    '''
    Class for the ToDo table in our database.
    Instances of this class correspond to rows in the table,
    where a row is an individual ToDo item.
    '''
    todo_id = pw.CharField( max_length = 32,
                              constraints=[
                                  pw.Check("LENGTH(todo_id) <= 32")
                              ]
                              )
    due_date = pw.CharField( max_length = 30,
                              constraints=[
                                  pw.Check("LENGTH(due_date) < 30")
                              ]
                              )
    todo_text = pw.CharField( max_length = 128,
                                constraints=[
                                    pw.Check("LENGTH(todo_text) < 128")
                                ]
                                )



class ToDoCollection():
    '''
    Class to organize methods that operate on todos.
    '''

    def __init__(self):
        logger.debug( "Initialize ToDoCollection" )

    def add_todo( self, new_todo_due_date, new_todo_id, new_todo_text ):
        '''
        add a new todo message to the collection
        '''
        logger.debug( "Entering method" )
        logger.debug( "Param: new_todo_id: " + new_todo_id )

        if self.search_todo( new_todo_id ):
            logger.debug( "ToDo already in database" )
            return False

        try:
            with db.transaction():
                new_todo = ToDoTable.create(
                    todo_id = new_todo_id,
                    due_date = new_todo_due_date,
                    todo_text = new_todo_text,
                )
                new_todo.save()

        except ( pw.DatabaseError,
                 pw.IntegrityError,
                 pw.NotSupportedError ) as db_exception:
            logger.info(f'Error creating todo = {new_todo_id}')
            logger.info(db_exception)
            return False

        else:
            logger.debug( "ToDo added" )
            return True

    def modify_todo( self, mod_todo_id, due_date, mod_todo_text ):
        '''
        Modifies an existing todo
        '''
        logger.debug( "Entering method" )
        logger.debug( "Param: mod_todo_id: " + mod_todo_id )
        logger.debug( "Param: mod_todo_text: " + mod_todo_text )

        todo_to_mod = self.search_todo( mod_todo_id )

        if todo_to_mod is None:
            logger.debug( "ToDo not in database" )
            return False

        try:
            with db.transaction():
                ToDoTable.update(
                    todo_text = mod_todo_text).where(
                        ( ToDoTable.todo_id == mod_todo_id)
                    and ( ToDoTable.due_date == due_date ) ).execute()  # noqa: E501 W503

            logger.debug(
                "todo_to_mod.todo_text: ", todo_to_mod.todo_text
            )

        except ( pw.DatabaseError,
                 pw.IntegrityError,
                 pw.NotSupportedError ) as db_exception:
            logger.info(f'Error modifying todo = {mod_todo_id}')
            logger.info(db_exception)

        logger.debug( "User updated" )
        return True

    def delete_todo( self, delete_todo_id ):
        '''
        Deletes a todo from todo_collection.

        Requirements:
        - Returns False if there are any errors (such as todo_id not found)
        - Otherwise, it returns True.
        '''
        logger.debug( "Entering function" )

        todo_to_del = self.search_todo( delete_todo_id )

        if todo_to_del is None:
            logger.debug( "ToDo not in database" )
            return False

        try:
            with db.transaction():
                todo_to_del.delete_instance(
                    #
                    # Ensure that we delete any dependent rows
                    #
                    recursive = True
                )

            logger.debug(
                "todo_to_del.todo_text: ", todo_to_del.todo_text
            )

        except ( pw.DatabaseError,
                 pw.IntegrityError,
                 pw.NotSupportedError ) as db_exception:
            logger.info(f'Error deleting todo = {delete_todo_id}')
            logger.info(db_exception)
            return False

        else:
            logger.debug( "ToDo deleted" )
            return True

    def search_todo( self, todo_id ):
        '''
        Searches for todo data
        '''
        logger.debug( "Entering method" )
        logger.debug( "Param: todo_id: " + todo_id )

        try:
            todo = ToDoTable.get_or_none(
                ToDoTable.todo_id == todo_id )

        except ( pw.DatabaseError,
                 pw.IntegrityError,
                 pw.NotSupportedError ) as db_exception:
            logger.info(f'Error searching for todo = {todo_id}')
            logger.info(db_exception)

        else:
            if todo:
                logger.debug( "ToDo ID found" )
                return todo
            logger.debug( "ToDo ID not in database" )
            return None

    def search_all_todo_updates( self, due_date ):
        '''
        Returns all the todo updates for a specified user.

        Requirements:
        - If the user is found, returns the corresponding
          ToDo instances as a list.
        - Otherwise, it returns None.
        '''
        logger.debug( "Entering method" )
        logger.debug( "Param: due_date: " + due_date )

        try:
            todo_list = ToDoTable.select().where(
                ToDoTable.due_date == due_date )

        except ( pw.DatabaseError,
                 pw.IntegrityError,
                 pw.NotSupportedError ) as db_exception:
            logger.info(f'Error searching for todos for {due_date}')
            logger.info(db_exception)

        else:
            if todo_list:
                logger.debug( "Todos for " + due_date + " found" )
                # pylint: disable=not-an-iterable
                return [ todo.todo_text for todo in todo_list ]
            logger.debug( "Due date: " + due_date + " not in database" )
            return None

    def filter_todo_by_string( self, target_string: str ):
        '''
        Returns all the todo updates for a specified user.

        Requirements:
        - Returns an iterator to all todo updates that contain the
          specified string. Note that there might not be any such todo
          updates . . . :-O
        '''
        logger.debug( "Entering method" )
        logger.debug( "Param: target_string: " + target_string )

        try:
            todo_iterator = ToDoTable.select() \
                .where( ToDoTable.todo_text.contains( target_string )) \
                .iterator()

        except ( pw.DatabaseError,
                 pw.IntegrityError,
                 pw.NotSupportedError ) as db_exception:
            logger.info(f'Error searching for todos {target_string}')
            logger.info(db_exception)

        else:
            if todo_iterator:
                logger.debug( "Iterator for " + target_string + " retrieved" )
                return todo_iterator
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

