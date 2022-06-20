
**Carl Parker | Python 320 | Assignment #7 | Sun 19 Jun 2022**

This project is more of a "proof of concept" than a finished app. Let me
explain what I have done here . . . 

I basically adapted the code for the peewee version of the social media
app to create the ToDo app. The available functionality is very basic,
but it demonstrates what I saw as the learning goals for the project:

- The app leverages pyschaffold and is installable using PIP.
- The app takes command line input and validates it using the cerberus
  module.
- The app leverages flask to support a web service, again with very
  basic functionality.

The project is available in the following public GitHub repo:

>  <https://github.com/carljparker/Python320-ToDoApp/tree/cajopa/assign7-dev>

Note that the project is in the `cajopa/assign7-dev` branch--as shown
above.

Also, I've prepared a (short) video that demonstrate the project's
functionality--described in detail below.


## Adapting the social media app ##

I removed the User functionality from the social media app--although
some vestiges of that code still remain. I then converted the schema for
status updates to repurpose them as as ToDo items: The `user_id` became
the due date. The status text became the ToDo text. The `status_id`
became the `todo_id`, but is no longer exposed to the user; instead, I
automatically assign a universally unique identifier (UUID) to the
`todo_item` when it is created.


## Command-line input ##

The app now responds differently depending on the command-line input.

- If the user specifies only the app name `todo.py`, then a much-hacked
  version of the menu system from the social-media app appears. The menu
  items _do_ work. For example, you can search ToDo items based on text
  string or due date.

- If the user specifies `todo.py web`, it starts the web server
  functionality which enables the user to get a list of the ToDo items
  by navigating to:

      http://127.0.0.1:5002/

  The web server can also be activated by just launching the module
  that implements the functionality:

      python3 tdweb.py

- If the user specifies `todo.py add <date> <ToDo text>`, the app will
  add the specified ToDo item. This is currently, the only ToDo CRUD[1]
  functionality available from the command line . . . :-(

- If the user specifies anything else on the command-line, they will get
  a help message.


[1] Create | Read | Update | Delete


### --- END --- ###

