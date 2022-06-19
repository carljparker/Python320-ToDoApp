'''
Provides a basic frontend
'''

# pylint: disable=C0301

import sys
import uuid
import cerberus as cerb

from loguru import logger


import main
import tdweb

logger.remove()
logger.add( sys.stderr, format="STDERR: {time:YYYY-MM-DD @ HH:mm:ss} | {level} | {file} : {function} : {line} : {message}", level="DEBUG" )
logger.add( "log_{time:YYYY-MM-DD}.log", format="LOGFILE: {time:YYYY-MM-DD @ HH:mm:ss} | {level} | {file} : {function} : {line} : {message}", level="DEBUG" )


def load_todo_updates():
    '''
    Loads todo updates from a file
    '''
    logger.debug( "Entering function" )
    filename = input('Enter filename for todo file: ')
    main.load_todo_updates(filename, todo_collection)

def add_todo_menu():
    '''
    Adds a new todo into the database
    '''
    logger.debug( "Entering function" )

    due_date = input('Due date: ')
    todo_text = input('ToDo text: ')
    add_todo( due_date, todo_text )

def add_todo( due_date, todo_text ):
    '''
    Adds a new todo into the database
    '''
    logger.debug( "Entering function" )
    #
    # Create the todo_id for the user
    #
    todo_id = uuid.uuid1().hex
    if not main.add_todo(due_date, todo_id, todo_text, todo_collection):
        print("An error occurred while trying to add new todo")
    else:
        print("New todo was successfully added")

def update_todo():
    '''
    Updates information for an existing todo
    '''
    logger.debug( "Entering function" )
    due_date = input('Due date: ')
    todo_id = input('ToDo ID: ')
    todo_text = input('ToDo text: ')
    if not main.update_todo(todo_id, due_date, todo_text,
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
        print(f"Due date: {result.due_date}")
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
    due_date = input('Enter due date for todos to retrieve: ')
    query_result_list = main.search_all_todo_updates(due_date, todo_collection)
    todo_gen = todo_generator( query_result_list )

    if not query_result_list:
        print("ERROR: No todos found" )
    else:
        print( f"A total of {str( len( query_result_list ) )} todo updates found for {due_date}" )
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

def menUX():
    menu_options = {
        'A': load_todo_updates,
        'B': add_todo_menu,
        'C': update_todo,
        'D': search_todo,
        'E': delete_todo,
        'F': search_all_todo_updates,
        'G': filter_todo_by_string,
        'H': flagged_todo_updates,
        'Q': quit_program
    }
    while True:
        user_selection = input("""
                            A: Load ToDo database
                            B: Add ToDo
                            C: Update ToDo
                            D: Search ToDo
                            E: Delete ToDo
                            F: Search ToDos by due date
                            G: Filter ToDos by string
                            H: Show all flagged ToDos
                            Q: Quit

                            Please enter your choice: """)
        user_selection_upper = user_selection.upper()
        if user_selection_upper in menu_options:
            menu_options[user_selection_upper]()
        else:
            print("Invalid option")

def start_webservice():
    print( "Starting webservice, access to ToDo list..." )
    print( "CTRL-C to shutdown webservice and exit" )
    print( "(Run tdweb.py to run webservice as a separate process.)" )
    print( "======================================================" )
    tdweb.start_webservice()

def print_help():
    '''
    Print help text to STDOUT
    '''
    print( "Usage: todo.py add <YYYY-MM-DD> <ToDo item>" )

if __name__ == '__main__':
    logger.debug( "Program start" )
    todo_collection = main.init_todo_collection()
    if len( sys.argv ) == 1:
        #
        # No cmdline params specified
        #
        menUX()
    if sys.argv[ 1 ] == "web":
        start_webservice() 
    #
    # Otherwise, parse the commandline
    #
    if sys.argv[ 1 ] == "add":
        cmd_params = {}
        cmd_params[ "due_date" ] = sys.argv[ 2 ]
        todo_text = " ".join( [ sys.argv[ n ] for n in range( 3, len( sys.argv ) ) ] )
        cmd_params[ "todo_text" ] = todo_text
        logger.debug( cmd_params[ "due_date" ] )
        logger.debug( cmd_params[ "todo_text" ] )

        #
        # Validate command-line parameters
        #
        v = cerb.Validator()
        schema = {
                'due_date': {'type': 'string', 'regex': '\d\d\d\d-\d\d-\d\d', 'maxlength': 10 },
                'todo_text': {'type': 'string', 'regex': '[a-zA-Z.,;: ]*' } 
                }
        document = cmd_params
        if v.validate(document, schema): 
            add_todo( cmd_params[ "due_date" ], cmd_params[ "todo_text" ] )
            quit_program()
        print( v.errors )
        quit_program()

    else:
        print_help()
        quit_program()


# --- END --- #

