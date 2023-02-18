#!/usr/bin/env python3

import sys
import argparse
from argparse import RawTextHelpFormatter

# Custom usage / help menu.
class HelpFormatter(argparse.HelpFormatter):
	def add_usage(self, usage, actions, groups, prefix=None):
		if prefix is None:
			prefix = ''
		return super(HelpFormatter, self).add_usage(
			usage, actions, groups, prefix)


# Custom help menu.
custom_usage = f"""
  
Backit
{'-'*100}
Usage Examples:
  python backit.py configs/pentest.ini
  python backit.py configs/pentest.ini --sendlog
  python backit.py configs/pentest.ini --keeplog --sendlog --showlog
"""

# Define parser
parser = argparse.ArgumentParser(formatter_class=HelpFormatter, description='', usage=custom_usage, add_help=True)

# Parser Options.
parser.add_argument('configfile', nargs="?", type=str, metavar='<configfile>', help="Input from configuration file")
parser.add_argument('--keeplog', action='store_true', help='Do not remove logfile.')
parser.add_argument('--sendlog', action='store_true', help='E-mail logfile')
parser.add_argument('--showlog', action='store_true', help='Print logfile')
parser.add_argument('--debug', action='store_true', help='Print SMTP Debug Information')

# Print 'help'.
if len(sys.argv) == 1 \
or sys.argv[0] == '-h' \
or sys.argv[0] == '--help':
	parser.print_help(sys.stderr)
	sys.exit(1)


if __name__ == "__main__":
	main()