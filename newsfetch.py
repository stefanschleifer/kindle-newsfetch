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
import subprocess
import glob

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
		recipes_path = raw_input("Please enter the absolute path to the directory where your recipes are stored [%s/recipes]: " % os.getcwd())
		if not recipes_path: # user chose to use default value
			recipes_path = "%s/recipes" % os.getcwd()
		# create the directory if it does not exist
		if not os.access(recipes_path, os.W_OK): os.mkdir(recipes_path)
		config.set('config', 'RECIPES_PATH', recipes_path)
		output_path = raw_input("Please enter the absolute path to the directory for storing the converted files [%s/tmp]: " % os.getcwd())
		if not output_path: # user chose to use default value
			output_path = "%s/tmp" % os.getcwd()
		# create the directory if it does not exist
		if not os.access(output_path, os.W_OK): os.mkdir(output_path)
		config.set('config', 'OUTPUT_PATH', output_path)
		config.set('config', 'SMTP_SERVER', raw_input("Please enter the address of your desired SMTP server: "))
		config.set('config', 'SMTP_USER', raw_input("Please enter the username for the given server: "))
		config.set('config', 'SMTP_PW', raw_input("Please enter the password for the given user (WILL BE STORED IN PLAINTEXT!): "))
		config.set('config', 'SMTP_MAILADDR', raw_input("Please enter your mail address for this server: ")) 
		ebook_convert = raw_input("Please enter the absolute path to 'ebook-convert' [/usr/bin/ebook-convert]: ")
		if not ebook_convert:
			ebook_convert = '/usr/bin/ebook-convert'
		config.set('config', 'EBOOK_CONVERT', ebook_convert)
		calibre_smtp = raw_input("Please enter the absolute path to 'calibre-smtp' [/usr/bin/calibre-smtp]: ")
		if not calibre_smtp:
			calibre_smtp = '/usr/bin/calibre-smtp'
		config.set('config', 'CALIBRE-SMTP', calibre_smtp)

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

	print "Successfully added item %s. Please add the required %s.recipe in %s now." % (name, recipe, config.get('config', 'recipes_path'))

# return a list of unique recipe names which
# should be converted in the current run
def collect_recipes(section='all', item=None):

	recipes = []

	config = ConfigParser.SafeConfigParser()
	config.read(CONFIGFILE)
	
	if item is None: # no request for specific item
		# all entries requested
		if 'all' == section:
			for section in config.sections():
				if section != 'config' and section != 'example':	
					for recipe, name in config.items(section):
						recipes.append(recipe)
		else: # all entries for specific section
			if config.has_section(section):
				for recipe, name in config.items(section):
					recipes.append(recipe)
			else:
				raise Exception("Section %s is not available in current configuration." % section)
	else: # specific entry
		for section in config.sections():
			if section != 'config' and section != 'example':
				for recipe, name in config.items(section):
					if item == recipe:
						recipes.append(item)
		if 0 == len(recipes): # no such recipe found
			raise Exception("Recipe named %s could not be found, please check the name and your configuration." % item)			

	# Attention: We're removing duplicate entries here, user hopefully expect this behavior!
	return list(set(recipes))

# convert a list of recipes to .mobi-format using ebook-convert
def convert_recipes(recipes):
	config = ConfigParser.SafeConfigParser()
	config.read(CONFIGFILE)
	recipes_path = config.get('config', 'recipes_path')
	output_path = config.get('config', 'output_path')
	ebook_convert = config.get('config', 'ebook-convert')

	for recipe in recipes:
		try:
			retcode = subprocess.call([ebook_convert, os.path.join(recipes_path, recipe + ".recipe"), os.path.join(output_path, recipe + ".mobi")])
			if 0 != retcode:
				raise Exception("Error while converting recipe %s" % recipe)
		except Exception ,e:
			print "Could not convert %s: %s." % ( os.path.join(recipes_path, recipe + ".mobi"), e)

# send all .mobi-files in defined output-directory
# to user via calibre-smtp
def send_ebooks():
	config = ConfigParser.SafeConfigParser()
	config.read(CONFIGFILE)
	calibre_smtp = config.get('config', 'calibre-smtp')
	
	# get all .mobi-files in output-dir
	files = glob.glob(config.get('config', 'output_path') + "/*.mobi")
	for f in files:
		try:
			retcode = subprocess.call([calibre_smtp, '-r', config.get('config', 'smtp_server'), '-u', config.get('config', 'smtp_user'), '-p', config.get('config', 'smtp_pw'), '-s', 'Send to Kindle', '-a', f, '-vv', config.get('config', 'smtp_mailaddr'), config.get('config', 'kindle_addr'), 'Send to Kindle'])
			if 0 != retcode:
				raise Exception("Error while sending .mobi-files via calibre-smtp.")
		except Exception, e:
			print "Could not send convertes files via mail: %s" % e

	cleanup()

# clean output direcotry
def cleanup():
	config = ConfigParser.SafeConfigParser()
	config.read(CONFIGFILE)
	output_path = config.get('config', 'output_path')	

	# get all .mobi-files in output-dir...
	files = glob.glob(config.get('config', 'output_path') + "/*.mobi")
	# ... and remove them
	for f in files:
		os.remove(f)

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

	if 'all' == sys.argv[1]: # convert and mail all configured items
		recipes = collect_recipes()
		convert_recipes(recipes)
	elif 'section' == sys.argv[1]: # convert and mail all items of a given section
		recipes = collect_recipes(sys.argv[2])
		convert_recipes(recipes)
	elif 'item' == sys.argv[1]: # convert and mail exactly one specific item
		recipes = collect_recipes(item=sys.argv[2])
		convert_recipes(recipes)
	elif 'add' == sys.argv[1]: # add a new configuration item
		try:
			add_item(sys.argv[2], sys.argv[3], sys.argv[4])
		except Exception, e:
			print "Could not add new item: %s" % e
		else:
			print "Successfully added item to configuration."
	elif 'list' == sys.argv[1]: # list all configured items
		try:
			list_all_items()
		except Exception, e:
			print "Could not list all items: %s" % e
	else:
		usage()


	
