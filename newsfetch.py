#!/usr/bin/env python

#
# newsfetch.py
#
# kindle-newsfetch is a simple Python script which fetches calibre recipes,
# turns them into Kindle newspapers using 'ebook-convert' and sends them to
# the configured Kindle e-mail adress using 'calibre-smtp'.
#
# (c) 2011 Stefan Schleifer, see LICENSE-file

import sys, os
import ConfigParser

# print help information
def usage():
	print "\nUsage: %s <command> [options]\n" % sys.argv[0]
	print "\tall: Fetch and convert all configured items."
	print "\tsection <section_name>: Fetch and convert all items of given section."
	print "\titem <item_name>: Only fetch and convert item named <item_name>."
	print "\tadd <item_name> <section_name>: Add a new item <item_name> to section <section_name>."
	print "\tlist: Get a list of all configured items."
	sys.exit(1)

# create configuraton file
def create_configuration():
	try:
		i = raw_input("I'm going to ask you a few questions and create newsfetch.cfg in the current working directory (%s), is this ok (y/n)? " % os.getcwd())
		if i is not 'y':
			print "Ok, not creating newsfetch.cfg for you. Bye!"
			sys.exit(1)

		config = ConfigParser.SafeConfigParser()
		config.add_section('config')
		config.set('config', 'KINDLE_ADDR', raw_input("Please enter your Kindle e-mail address where you want the converted files to be delivered to: "))
		config.set('config', 'OUTPUT_PATH', raw_input("Please enter the absolute path to the directory for storing the converted files: "))
		config.set('config', 'SMTP_SERVER', raw_input("Please enter the address of your desired SMTP server: "))
		config.set('config', 'SMTP_USER', raw_input("Please enter the username for the given server: "))
		config.set('config', 'SMTP_PW', raw_input("Please enter the password for the given user, WILL BE STORED IN PLAINTEXT: "))

		config.add_section('example')
		config.set('example', 'nytimes', 'New York Times')
		config.set('example', 'sueddeutsche', 'Sueddeutsche Zeitung')

		with open('newsfetch.cfg', 'w') as configfile:
			config.write(configfile)

	except Exception, e:
		print "Could not create newsfetch.cfg: %s" % e
	else:
		print "Successfully created newsfetch.cfg. We've added example entries too."

# list all configured items with their names
def list_all_items():
	print "not implemented yet"

# return a list of unique recipe names which
# should be converted in the current run
def collect_recipes(section='all'):
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
			create_configuration()
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
		list_all_items()
	else:
		usage()


	
