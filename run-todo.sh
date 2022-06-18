#
# Run this script from the top-level directory. For example:
#
#     ~/git/github/Python320-ToDoApp
#

#
# Need to set the PYTHONPATH so that the tests can find and import the
# modules in `src` to be tested.
#
export PYTHONPATH=$PYTHONPATH:~/git/github/Python320-ToDoApp/src

rm td.db & python3 src/todo.py $@


# --- END --- #

