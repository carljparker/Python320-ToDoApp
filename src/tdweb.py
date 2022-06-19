
from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import jsonify


class Todo(Resource):
    '''
    Class to surface ToDo list table as a RESTful resource
    '''
    def get(self):
        '''
        Code that responds to an HTTP GET request on the ToDo list
        resource
        '''
        conn = db_connect.connect()
        query = conn.execute("SELECT todo_id, due_date, todo_text FROM todotable;")
        result = {"data": [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        conn.close()
        return jsonify(result)

def start_webservice():
    '''
    Start the RESTful web service

    This function can be called from external code or from the __main__
    code block below.
    '''
    #
    # Create these variables at global scope, used by both this function
    # and the Todo class.
    #
    global db_connect
    global api
    global app

    db_connect = create_engine("sqlite:///td.db")

    app = Flask(__name__)

    api = Api(app)
    api.add_resource(Todo, "/")  # Route_1

    app.run(port="5002")

    db_connect.dispose()

if __name__ == "__main__":
    start_webservice()


