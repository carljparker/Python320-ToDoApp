'''
Provides a basic frontend
'''

# pylint: disable=C0301

import sys

from loguru import logger

import main

logger.remove()
logger.add( sys.stderr, format="STDERR: {time:YYYY-MM-DD @ HH:mm:ss} | {level} | {file} : {function} : {line} : {message}", level="DEBUG" )
logger.add( "log_{time:YYYY-MM-DD}.log", format="LOGFILE: {time:YYYY-MM-DD @ HH:mm:ss} | {level} | {file} : {function} : {line} : {message}", level="DEBUG" )


def load_users():
    '''
    Loads user accounts from a file
    '''
    logger.debug( "Entering function" )
    filename = input('Enter filename of user file: ')
    main.load_users(filename, user_collection)


def load_todo_updates():
    '''
    Loads todo updates from a file
    '''
    logger.debug( "Entering function" )
    filename = input('Enter filename for todo file: ')
    main.load_todo_updates(filename, todo_collection)


def save_users():
    '''
    Saves user database into a file
    '''
    logger.debug( "Entering function" )
    filename = input('Enter filename for users file: ')
    main.save_users(filename, user_collection)


def add_todo():
    '''
    Adds a new todo into the database
    '''
    logger.debug( "Entering function" )
    user_id = input('User ID: ')
    todo_id = input('ToDo ID: ')
    todo_text = input('ToDo text: ')
    if not main.add_todo(user_id, todo_id, todo_text, todo_collection):
        print("An error occurred while trying to add new todo")
    else:
        print("New todo was successfully added")


def update_todo():
    '''
    Updates information for an existing todo
    '''
    logger.debug( "Entering function" )
    user_id = input('User ID: ')
    todo_id = input('ToDo ID: ')
    todo_text = input('ToDo text: ')
    if not main.update_todo(todo_id, user_id, todo_text,
                              todo_collection):
        print("An error occurred while trying to update todo")
    else:
        print("ToDo was successfully updated")


def search_todo():
    '''
    Searches a todo in the database
    '''
    logger.debug( "Entering function" )
    todo_id = input('Enter todo ID to search: ')
    result = main.search_todo(todo_id, todo_collection)
    if not result:
        print("ERROR: ToDo does not exist")
    else:
        print(f"User ID: {result.user_id}")
        print(f"ToDo ID: {result.todo_id}")
        print(f"ToDo text: {result.todo_text}")


def delete_todo():
    '''
    Deletes todo from the database
    '''
    logger.debug( "Entering function" )
    todo_id = input('ToDo ID: ')
    if not main.delete_todo(todo_id, todo_collection):
        print("An error occurred while trying to delete todo")
    else:
        print("ToDo was successfully deleted")


def save_todo():
    '''
    Saves todo database into a file
    '''
    logger.debug( "Entering function" )
    filename = input('Enter filename for todo file: ')
    main.save_todo_updates(filename, todo_collection)

def todo_generator( query_result_list ):
    '''
    Take a list and turn it into a generator
    '''
    logger.debug( "Entering function" )
    assert len( query_result_list )

    for todo in query_result_list:
        yield todo

def search_all_todo_updates():
    '''
    Searches a todo in the database
    '''
    logger.debug( "Entering function" )
    user_id = input('Enter user ID for todos to retrieve: ')
    query_result_list = main.search_all_todo_updates(user_id, todo_collection)
    todo_gen = todo_generator( query_result_list )

    if not query_result_list:
        print("ERROR: No todos found" )
    else:
        print( f"A total of {str( len( query_result_list ) )} todo updates found for {user_id}" )
        while True:
            user_response = input('Would you like to see the next update? (Y/N): ')
            if user_response.upper() == "Y":
                try:
                    print( next( todo_gen ) )

                except StopIteration:
                    print( "No more todo updates . . . :-(" )
                    break
            else:
                break

def filter_todo_by_string():
    '''
    Searches a todo in the database
    '''
    logger.debug( "Entering function" )
    target_text = input('Enter todo text on which to filter: ')
    todo_iterator = main.filter_todo_by_string( target_text, todo_collection)

    if not todo_iterator:
        print("ERROR: No iterator returned" )
    else:
        while True:
            user_response = input('Review the next todo? (Y/N): ')
            if user_response.upper() == "Y":
                try:
                    current_todo = next( todo_iterator )
                    print( current_todo.todo_text )
                    delete_response = input('Delete this todo? (Y/N): ')
                    if delete_response.upper() == "Y":
                        main.delete_todo( current_todo.todo_id, todo_collection )

                except StopIteration:
                    print( "No more todo updates . . . :-(" )
                    break
            else:
                break

def flagged_todo_updates():
    '''
    Searches a todo in the database
    '''
    logger.debug( "Entering function" )
    target_text = input('Enter todo text for flagging: ')
    todo_iterator = main.filter_todo_by_string( target_text, todo_collection)

    # pylint: disable=expression-not-assigned
    if not todo_iterator:
        print("ERROR: No iterator returned" )
    else:
        [ print( str( statu.todo_id ) + ": " + statu.todo_text )
          for statu in todo_iterator ]

def quit_program():
    '''
    Quits program
    '''
    logger.debug( "Entering function" )
    sys.exit()


if __name__ == '__main__':
    logger.debug( "Program start" )
    user_collection = main.init_user_collection()
    todo_collection = main.init_todo_collection()
    menu_options = {
        'A': load_users,
        'B': load_todo_updates,
        'H': add_todo,
        'I': update_todo,
        'J': search_todo,
        'K': delete_todo,
        'L': save_todo,
        'M': search_all_todo_updates,
        'N': filter_todo_by_string,
        'O': flagged_todo_updates,
        'Q': quit_program
    }
    while True:
        user_selection = input("""
                            A: Load user database
                            B: Load todo database
                            G: Save user database to file
                            H: Add todo
                            I: Update todo
                            J: Search todo
                            K: Delete todo
                            L: Save todo database to file
                            M: Search all todo updates
                            N: Filter todo updates by string
                            O: Show all flagged todo updates
                            Q: Quit

                            Please enter your choice: """)
        user_selection_upper = user_selection.upper()
        if user_selection_upper in menu_options:
            menu_options[user_selection_upper]()
        else:
            print("Invalid option")
