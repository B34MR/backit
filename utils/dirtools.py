#!/usr/bin/env python3

import os
import logging


def mkdir(directory):
	''' 
	Create dir, log if dir already exists.
	arg(s):directory:str
	'''
	try:
		os.makedirs(directory, exist_ok = False)
	except FileExistsError as e:
		logging.info(f'{e}')
		pass
	else:	
		return directory


def lsdir(directory):
	''' 
	List files and file size from directory.
	arg(s):directory:str
	'''
	
	item_size = []
	# Create a lst files.
	files_list = filter(
		lambda x : os.path.isfile(os.path.join(directory, x)),
		os.listdir(directory)
		)	
	# Get file size(s).
	size_of_file = [
	    (item, os.stat(os.path.join(directory, item)).st_size)
	    for item in files_list
	]	
	# Return files and size from lst.
	for item, size in sorted(size_of_file):
		item_size.append(f"{item}: {round(size/(1024*1024), 3)} MB")
	return item_size