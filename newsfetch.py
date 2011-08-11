#!/usr/bin/env python

#
# newsfetch.py
#
# kindle-newsfetch is a simple Python script which fetches calibre recipes,
# turns them into Kindle newspapers using 'ebook-convert' and sends them to
# the configured Kindle e-mail adress using 'calibre-smtp'.
#
# (c) 2011 Stefan Schleifer, see LICENSE-file

import sys
import ConfigParser

def usage():
	print "\nUsage: %s <command> [options]\n" % sys.argv[0]
	print "\tall: Fetch and convert all configured items."
	print "\tsection <section_name>: Fetch and convert all items of given section."
	print "\titem <item_name>: Only fetch and convert item named <item_name>."
	print "\tadd <item_name> <section_name>: Add a new item <item_name> to section <section_name>."
	print "\tlist: Get a list of all configured items."
	sys.exit(1)

def create_configfile():
	pass

def list_items():
	print "not implemented yet"

if '__main__' == __name__:

	if not len(sys.argv) > 1:
		usage()

	# check if config file newsfetch.cfg exists
	# or promt to create one
	try:
		with open('newsfetch.cfg', 'r') as configfile:
			print "Configfile exists..."
	except:
		i = raw_input("Neccessary file newsfetch.cfg could not be found, do you want to create it now (y/n)? ")
		if 'y' == i:
			create_configfile()
		else:
			print "Cannot continue without configuration file. Either rerun %s and let it create newsfetch.cfg for you or create it manually. See example.cfg for possible options/values." % sys.argv[0]
			sys.exit(1)

	if 'all' == sys.argv[1]:
		pass
	elif 'section' == sys.argv[1]:
		pass
	elif 'item' == sys.argv[1]:
		pass
	elif 'add' == sys.argv[1]:
		pass
	elif 'list' == sys.argv[1]:
		list_items()
	else:
		usage()


	
