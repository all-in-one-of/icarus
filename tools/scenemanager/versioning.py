#!/usr/bin/python

# [scenemanager] versioning.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Controls versioning of files.


import os
import re

# Import custom modules
from shared import os_wrapper
from shared import verbose


__padding__ = 3
__min_version__ = 0
__max_version__ = 999


def get_latest(file_list):
	""" Detect the latest version of a file from the provided list of files.
		Return a list of files containing only the latest versions.
	"""
	seq = get_versions(file_list)
	matches = []
	# print "\n---debug---"
	# import json
	# print(json.dumps(seq, indent=4, sort_keys=True))
	# print "-----------\n"

	# Find latest version
	for prefix, value in seq.iteritems():
		versions = []
		for ver, path in value.iteritems():
			versions.append(int(ver))
		# print prefix, max(versions)
		latest = max(versions)
		matches.append(value[latest])

	return matches


def get_versions(file_list):
	""" Detect versions of a file from the provided list of files.
		Return a nested dictionary in the format:

		base_file_prefix: {
			version: filepath, 
			version: filepath
		}, 
		base_file_prefix: {
			version: filepath
		}
		...
		etc.
	"""
	seq = {}

	for filepath in file_list:
		filepath = os_wrapper.absolutePath(filepath)
		meta = parse(filepath)
		if '<description>' in meta:
			prefix = ".".join([meta['<shot>'], meta['<discipline>'], meta['<description>']])
		else:
			prefix = ".".join([meta['<shot>'], meta['<discipline>']])
		v_int = version_to_int(meta['<version>'])
		try:
			seq[prefix][v_int] = filepath
		except KeyError:
			seq[prefix] = {v_int: filepath}

	return seq


def parse(filepath, 
	      base_dir=os_wrapper.absolutePath('$SCNMGR_SAVE_DIR/..'), 
	      convention=os.environ['SCNMGR_CONVENTION']):
	""" Parse the given filepath (relative to base_dir) based on a naming
		convention and return a dictionary of elements for processing.
		TODO: check shot, artist, discipline etc. against valid whitelist
	"""
	if not os.path.isfile(filepath):
		verbose.print_("Could not parse filename as file doesn't exist: %s" % filepath)
		return None

	filepath = os.path.normpath(filepath)
	base_dir = os.path.normpath(base_dir)

	# Make filepath relative to base_dir
	if filepath.startswith(base_dir):
		filepath = filepath.replace(base_dir, '', 1)
		filepath = filepath.replace('\\', '/')  # Convert to forward slashes
		if filepath.startswith('/'):
			filepath = filepath.replace('/', '', 1)  # Remove leading slash


	# Find optional parts in naming convention
	# (only one optional section is allowed, if there are more, all optional
	# parts will be ignored.)
	valid_conventions = [convention.replace('[', '').replace(']', '')]
	pattern = r'\[.+?\]'
	optionals = re.findall(pattern, convention)
	if len(optionals) == 1:
		for i, optional in enumerate(optionals):
			valid_conventions.append(convention.replace(optional, '', i+1))
	# print valid_conventions

	# # Find tokens in naming convention
	# pattern = r'<\w+>'
	# tokens = re.findall(pattern, convention)

	# # Remove duplicates & sort list
	# tokens = list(set(tokens))
	# # tokens.sort()
	# print tokens

	# # Generate regular expression to represent naming convention

	token_dict = {}
	success = False
	f = explode_path(filepath)
	for con in valid_conventions:
		c = explode_path(con)

		if same_structure(f, c):
			for i, dirs in enumerate(c):
				for j, token in enumerate(dirs):
					value = f[i][j]
					if token in token_dict:  # Sanity check duplicated tokens
						if token_dict[token] != value:
							verbose.error("Could not parse filename due to a token value mismatch.")
							return None
					else:
						token_dict[token] = value

			success = True

	if success:
		# print(token_dict)
		return token_dict

	else:
		msg = "The filename '%s' could not be parsed because it does not comply with the naming convention." % filepath
		for con in valid_conventions:
			msg += "\n" + con
		verbose.error(msg)
		return None


def explode_path(filepath):
	""" Return a list from a path. First split into directories, then by a
		delimiter character such as '.'
	"""
	path_elem = []
	for d in filepath.split('/'):
		path_elem.append(d.split('.'))
	return path_elem


def same_structure(a, b):
	""" Check if two exploded paths (a and b) have the same structure.
	"""
	x = []; y = []
	for i in a:
		x.append(len(i))
	for j in b:
		y.append(len(j))
	if x==y:
		return True
	else:
		return False


def version_to_int(v_str):
	""" Convert a version string in the format 'vXXX' to an integer.
	"""
	# if v_str.startswith('v'):
	return int(v_str.replace('v', '', 1))


def version_up(base_file):
	""" Upversion the given file.
	"""
	pass


def version(input_version, increment):
	""" Change the version number.
	"""
	new_version = input_version + increment
	if __min_version__ <= new_version <= __max_version__:
		return new_version
	else:
		verbose.error("Version number out of bounds.")
		return input_version

