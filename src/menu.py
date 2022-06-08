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


def load_status_updates():
    '''
    Loads status updates from a file
    '''
    logger.debug( "Entering function" )
    filename = input('Enter filename for status file: ')
    main.load_status_updates(filename, status_collection)


def add_user():
    '''
    Adds a new user into the database
    '''
    logger.debug( "Entering function" )
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.add_user(user_id,
                         email,
                         user_name,
                         user_last_name,
                         user_collection):
        print("An error occurred while trying to add new user")
    else:
        print("User was successfully added")


def update_user():
    '''
    Updates information for an existing user
    '''
    logger.debug( "Entering function" )
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.update_user(
        user_id,
        email,
        user_name,
        user_last_name,
        user_collection
    ):
        print("An error occurred while trying to update user")
    else:
        print("User was successfully updated")


def search_user():
    '''
    Searches a user in the database
    '''
    logger.debug( "Entering function" )
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id, user_collection)
    if not result:
        print("ERROR: User does not exist")
    else:
        print(f"User ID: {result.user_id}")
        print(f"Email: {result.email}")
        print(f"Name: {result.user_name}")
        print(f"Last name: {result.user_last_name}")


def delete_user():
    '''
    Deletes user from the database
    '''
    logger.debug( "Entering function" )
    user_id = input('User ID: ')
    if not main.delete_user(user_id, user_collection):
        print("An error occurred while trying to delete user")
    else:
        print("User was successfully deleted")


def save_users():
    '''
    Saves user database into a file
    '''
    logger.debug( "Entering function" )
    filename = input('Enter filename for users file: ')
    main.save_users(filename, user_collection)


def add_status():
    '''
    Adds a new status into the database
    '''
    logger.debug( "Entering function" )
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.add_status(user_id, status_id, status_text, status_collection):
        print("An error occurred while trying to add new status")
    else:
        print("New status was successfully added")


def update_status():
    '''
    Updates information for an existing status
    '''
    logger.debug( "Entering function" )
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.update_status(status_id, user_id, status_text,
                              status_collection):
        print("An error occurred while trying to update status")
    else:
        print("Status was successfully updated")


def search_status():
    '''
    Searches a status in the database
    '''
    logger.debug( "Entering function" )
    status_id = input('Enter status ID to search: ')
    result = main.search_status(status_id, status_collection)
    if not result:
        print("ERROR: Status does not exist")
    else:
        print(f"User ID: {result.user_id}")
        print(f"Status ID: {result.status_id}")
        print(f"Status text: {result.status_text}")


def delete_status():
    '''
    Deletes status from the database
    '''
    logger.debug( "Entering function" )
    status_id = input('Status ID: ')
    if not main.delete_status(status_id, status_collection):
        print("An error occurred while trying to delete status")
    else:
        print("Status was successfully deleted")


def save_status():
    '''
    Saves status database into a file
    '''
    logger.debug( "Entering function" )
    filename = input('Enter filename for status file: ')
    main.save_status_updates(filename, status_collection)

def status_generator( query_result_list ):
    '''
    Take a list and turn it into a generator
    '''
    logger.debug( "Entering function" )
    assert len( query_result_list )

    for status in query_result_list:
        yield status

def search_all_status_updates():
    '''
    Searches a status in the database
    '''
    logger.debug( "Entering function" )
    user_id = input('Enter user ID for statuses to retrieve: ')
    query_result_list = main.search_all_status_updates(user_id, status_collection)
    status_gen = status_generator( query_result_list )

    if not query_result_list:
        print("ERROR: No statuses found" )
    else:
        print( f"A total of {str( len( query_result_list ) )} status updates found for {user_id}" )
        while True:
            user_response = input('Would you like to see the next update? (Y/N): ')
            if user_response.upper() == "Y":
                try:
                    print( next( status_gen ) )

                except StopIteration:
                    print( "No more status updates . . . :-(" )
                    break
            else:
                break

def filter_status_by_string():
    '''
    Searches a status in the database
    '''
    logger.debug( "Entering function" )
    target_text = input('Enter status text on which to filter: ')
    status_iterator = main.filter_status_by_string( target_text, status_collection)

    if not status_iterator:
        print("ERROR: No iterator returned" )
    else:
        while True:
            user_response = input('Review the next status? (Y/N): ')
            if user_response.upper() == "Y":
                try:
                    current_status = next( status_iterator )
                    print( current_status.status_text )
                    delete_response = input('Delete this status? (Y/N): ')
                    if delete_response.upper() == "Y":
                        main.delete_status( current_status.status_id, status_collection )

                except StopIteration:
                    print( "No more status updates . . . :-(" )
                    break
            else:
                break

def flagged_status_updates():
    '''
    Searches a status in the database
    '''
    logger.debug( "Entering function" )
    target_text = input('Enter status text for flagging: ')
    status_iterator = main.filter_status_by_string( target_text, status_collection)

    # pylint: disable=expression-not-assigned
    if not status_iterator:
        print("ERROR: No iterator returned" )
    else:
        [ print( str( statu.status_id ) + ": " + statu.status_text )
          for statu in status_iterator ]

def quit_program():
    '''
    Quits program
    '''
    logger.debug( "Entering function" )
    sys.exit()


if __name__ == '__main__':
    logger.debug( "Program start" )
    user_collection = main.init_user_collection()
    status_collection = main.init_status_collection()
    menu_options = {
        'A': load_users,
        'B': load_status_updates,
        'C': add_user,
        'D': update_user,
        'E': search_user,
        'F': delete_user,
        'G': save_users,
        'H': add_status,
        'I': update_status,
        'J': search_status,
        'K': delete_status,
        'L': save_status,
        'M': search_all_status_updates,
        'N': filter_status_by_string,
        'O': flagged_status_updates,
        'Q': quit_program
    }
    while True:
        user_selection = input("""
                            A: Load user database
                            B: Load status database
                            C: Add user
                            D: Update user
                            E: Search user
                            F: Delete user
                            G: Save user database to file
                            H: Add status
                            I: Update status
                            J: Search status
                            K: Delete status
                            L: Save status database to file
                            M: Search all status updates
                            N: Filter status updates by string
                            O: Show all flagged status updates
                            Q: Quit

                            Please enter your choice: """)
        user_selection_upper = user_selection.upper()
        if user_selection_upper in menu_options:
            menu_options[user_selection_upper]()
        else:
            print("Invalid option")
