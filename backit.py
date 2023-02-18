#!/usr/bin/env python3

from configparser import ConfigParser
from datetime import datetime
from functools import wraps
from utils import arguments
from utils.colors import Colors as c
from utils import dirtools
from utils import mailer
import os
import sys
import tarfile
import time


# Argparse - init and parse.
args = arguments.parser.parse_args()

# Args - Config filepath.
config_fp = args.configfile

# Argparse - Debug level.
debuglevel = 0
debuglevel = 1 if args.debug else debuglevel 

# ConfigParser - init and defined instance options.
config = ConfigParser(allow_no_value=True, delimiters='=')
config.optionxform = str

# Config name provided on cli.
config_name = os.path.basename(config_fp)


def timeit(method):
	'''Wrapper to calculate execution time'''
	@wraps(method)
	def wrapper(*args, **kargs):
		starttime = time.time()
		result = method(*args, **kargs)
		endtime = time.time()
		print(f'\n')
		print(f'Completed in: {(endtime-starttime)*1000} ms')
		return result
	return wrapper


def time_stamp():
	'''Time Stamp used for start/stop and archive filename'''
	current_time = datetime.now()
	return current_time.strftime('%b-%d-%y-%H-%M-%S')


def do_backup(archive_dest, source_dir):
	'''Create TAR backup job'''
	with tarfile.open(archive_dest, 'w:gz') as tar:
		for data in source_dir:
			tar.add(data)
		return tar


def get_tarmembers(filepath):
	'''Read TAR archive and create a members lst'''
	try:
		if tarfile.is_tarfile(filepath):
			with tarfile.open(filepath, 'r') as tar:
				tar_members_lst = tar.getmembers()
	except Exception as e:
		print(f'[!] ERROR: TAR file check failed: {e}')
	else:
		return tar_members_lst

@timeit
def main():
	'''Main func'''

	# ConfigParser - clear config cache and read newconfig file.
	config.clear()
	config.read(config_fp)

	# Backup list via config.ini.
	SOURCE_LST = [i for i in config['source']]

	# Backup destination via config.ini.
	DEST_DIR = ' '.join([i for i in config['destination']])

	# SMTP server settings via config.ini.
	SMTP_SETTINGS = {k:v for k, v in config['smtp_settings'].items()}

	# SMTP headers via config.ini.
	SMTP_AUTH = {k:v for k, v in config['smtp_auth'].items()}
	
	# SMTP headers via config.ini.
	SMTP_HEADERS = {k:v for k, v in config['smtp_headers'].items()}

	# Archive filepath and log file, time stamped.
	TS = time_stamp()
	DEST_FP = os.path.join(DEST_DIR, f'archive-{TS}.tar.gz')
	LOG_FILE = f'log_{TS}.txt'

	# Print Job info to STDOUT.
	print(f'[*] Config: {config_name}')
	print(f'[*] Source: {SOURCE_LST}')
	print(f'[*] Destination: {DEST_DIR}')
	print(f'[*] SMTP Server: {SMTP_SETTINGS}')
	print(f'[*] E-mail: {SMTP_HEADERS}')

	# Sanity Check - Destination dir.
	print(f"[*] Sanity Checking: 'Source' and 'Destination'")
	if not os.path.exists(f"{DEST_DIR}"):
		print(f'[{c.RED}-{c.END}] Destination does not exist: {DEST_DIR}')
		print(f'[*] Exiting')
		sys.exit(1)

	# Sanity Check - Source lst.
	REMOVED_SOURCES = [i for i in SOURCE_LST if not os.path.exists(f"{i}")]
	SOURCE_LST = [i for i in SOURCE_LST if os.path.exists(f"{i}")]
	# Print source updated.
	if REMOVED_SOURCES:
		print(f'[{c.RED}-{c.END}] Source does not exist: {REMOVED_SOURCES}')
		print(f'[{c.YELLOW}*{c.END}] Source Updated: {SOURCE_LST}')
	# sys.exit()

	# Run Backup
	try:
		ts_start = time_stamp()
		my_tarfile = do_backup(DEST_FP, SOURCE_LST)
		ts_end = time_stamp()
		backup_status = 'success'
		print(f'[{c.GREEN}*{c.END}] Backup Status: {backup_status.upper()}')
		print(f'[*] Backup File: {os.path.join(DEST_DIR, my_tarfile.name)}')	
	except Exception as e:
		print(f'[!] ERROR: Backup Backup failed: {e}')
		backup_status = 'failed'
		print(f'[{c.RED}-{c.END}] Backup Status: {backup_status.upper()}')
	except KeyboardInterrupt:
		keyboard_interrupt()
	
	# Write log file.
	with open(LOG_FILE, 'w') as f1:
		f1.write(f'\nBackup Log\n')
		f1.write(f'{"-"*45}\n')
		f1.write(f'Backup Status: {backup_status.upper()}\n')
		f1.write(f'Source(s): {SOURCE_LST}\n')
		f1.write(f'Destination: {DEST_DIR}\n')
		f1.write(f'Started: {ts_start}\n')
		f1.write(f'Completed: {ts_end}\n')
		f1.write(f'Archive Name: {my_tarfile.name}\n')
		
		f1.write(f'\nArchive Contents\n')
		f1.write(f'{"-"*45}\n')
		tar_members_lst = get_tarmembers(DEST_FP)
		[f1.write(f'{str(i)}\n') for i in tar_members_lst]

		f1.write(f'\nDestination Directory: {DEST_DIR}\n')
		f1.write(f'{"-"*45}\n')
		file_list = dirtools.lsdir(DEST_DIR)
		[f1.writelines(f'{i}\n') for i in file_list]

	# Email log file.
	if args.sendlog:
		print(f'[*] E-mail Attachment: {LOG_FILE}')
		my_mailer = mailer.Mailer(
			SMTP_SETTINGS['host'], 
			SMTP_SETTINGS['port'],
			debuglevel
			)
		
		my_mailer.login(
			SMTP_AUTH['username'], 
			SMTP_AUTH['password']
			)
		my_mailer.send_msg_attachment(
			SMTP_HEADERS['from'],
			SMTP_HEADERS['to'],
			SMTP_HEADERS['subject'],
			LOG_FILE
			)

	# Print log file to STDOUT.
	if args.showlog:
		with open(LOG_FILE, 'r') as f1:
			print(f1.read())

	# Delete log file.
	if not args.keeplog:
		try:
			os.remove(LOG_FILE)
			print(f'[*] Removed: {LOG_FILE}')	
		except OSError:
			pass

if __name__ == '__main__':
	main()