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

# full path to configuration file
CONFIGFILE = '/Users/stefan/.src/kindle-newsfetch/newsfetch.cfg'

# print help information
def usage():
	print "\nUsage: %s <command> [options]\n" % sys.argv[0]
	print "\tall: Fetch and convert all configured items."
	print "\tsection <section_name>: Fetch and convert all items of given section."
	print "\titem <item_name>: Only fetch and convert item named <item_name>."
	print "\tadd <recipe_name> <item_name> <section_name>: Add a new item <item_name> with recipe-id <recipe_name> to section <section_name>."
	print "\tlist: Get a list of all configured items."
	sys.exit(1)

# create configuraton file
def create_configuration():
	try:
		i = raw_input("I'm going to ask you a few questions and create %s, is this ok (y/n)? " % CONFIGFILE)
		if i is not 'y':
			print "Ok, not creating configuration file. Bye!"
			sys.exit(1)

		config = ConfigParser.SafeConfigParser()
		config.add_section('config')
		config.set('config', 'KINDLE_ADDR', raw_input("Please enter your Kindle e-mail address where you want the converted files to be delivered to: "))
		config.set('config', 'OUTPUT_PATH', raw_input("Please enter the absolute path to the directory for storing the converted files: "))
		config.set('config', 'SMTP_SERVER', raw_input("Please enter the address of your desired SMTP server: "))
		config.set('config', 'SMTP_USER', raw_input("Please enter the username for the given server: "))
		config.set('config', 'SMTP_PW', raw_input("Please enter the password for the given user (WILL BE STORED IN PLAINTEXT!): "))

		config.add_section('example')
		config.set('example', 'nytimes', 'New York Times')
		config.set('example', 'sueddeutsche', 'Sueddeutsche Zeitung')

		with open(CONFIGFILE, 'w') as configfile:
			config.write(configfile)

	except Exception, e:
		print "Could not create %s: %s" % (CONFIGFILE, e)
	else:
		print "Successfully created %s. We've added a few example entries too." % CONFIGFILE
		sys.exit(0)

# list all configured items with their names
def list_all_items():
	config = ConfigParser.SafeConfigParser()
	config.read(CONFIGFILE)
	for section in config.sections():
		# ignore config and example sections
		if section != 'config' and section != 'example':
			print "Section: %s" % section
			for recipe, name in config.items(section):
				print "\t%s (%s)" % (name, recipe)

# add a new configuration item
def add_item(recipe, name, section):

	config = ConfigParser.SafeConfigParser()
	config.read(CONFIGFILE)

	# check if section already exists
	try:
		config.add_section(section)
	except ConfigParser.DuplicateSectionError, ValueError:
		pass

	# entry already exists, asking whether to replace it
	if config.has_option(section, recipe):
		i = raw_input("Recipe %s with name %s already exists in section %s, do you want to update it (y/n)? " % (recipe, config.get(section, recipe), section))
		if i is not 'y':
			raise Exception("Adding item aborted by user as the item already exists.")
		
	config.set(section, recipe, name)

	with open(CONFIGFILE, 'w') as configfile:
		config.write(configfile)

# return a list of unique recipe names which
# should be converted in the current run
def collect_recipes(section='all'):
	print "not implemented yet"

if '__main__' == __name__:

	if not len(sys.argv) > 1:
		usage()

	# check if configuration file exists
	# or promt to create one
	try:
		with open(CONFIGFILE, 'r') as configfile:
			pass
	except:
		i = raw_input("Neccessary configuration file %s could not be found, do you want to create it now (y/n)? " % CONFIGFILE)
		if 'y' == i:
			create_configuration()
		else:
			print "Cannot continue without configuration file. Either rerun %s and let it create the configuration file for you or create it manually. See example.cfg for possible options/values." % sys.argv[0]
			sys.exit(1)

	if 'all' == sys.argv[1]:
		pass
	elif 'section' == sys.argv[1]:
		pass
	elif 'item' == sys.argv[1]:
		pass
	elif 'add' == sys.argv[1]:
		try:
			add_item(sys.argv[2], sys.argv[3], sys.argv[4])
		except Exception, e:
			print "Could not add new item: %s" % e
		else:
			print "Successfully added item to configuration."
	elif 'list' == sys.argv[1]:
		try:
			list_all_items()
		except Exception, e:
			print "Could not list all items: %s" % e
	else:
		usage()


	
