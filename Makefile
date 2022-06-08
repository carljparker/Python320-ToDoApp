SHELL = /bin/bash

#
# Special target so that all lines of my recipes execute in a single
# instance of the above-specified shell.
#
.ONESHELL:

clean:
	rm accounts-new.csv
	rm accounts-with-delete.csv
	rm status_updates-new.csv
	rm status_updates-with-mod.csv
	rm status_updates-with-delete.csv
	rm accounts-with-deleted-alcon.csv
	rm status_updates-with-deletion.csv
	rm log*.log
	rm Session.vim
	
