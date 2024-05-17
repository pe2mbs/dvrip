from getopt import GetoptError, getopt
from socket import gethostbyname
from sys import stderr
from typing import List, NoReturn
from dvrip import __version__
from dvrip.io import DVRIPClient
from dvrip.cmd import EX_USAGE, EX_NOHOST, guard, osexit, prog


def usage() -> NoReturn:
	print('Usage: {} discover'.format(prog()), file=stderr)
	exit(EX_USAGE)


def run(args: List[str]) -> None:
	try:
		opts, args = getopt(args, 'i:t:')
	except GetoptError:
		usage()
	if args:
		usage()

	interface = ''
	timeout   = 1.0
	for opt, arg in opts:
		if opt == '-i':
			try:
				interface = gethostbyname(arg)
			except OSError as e:
				osexit(e, EX_NOHOST)
		if opt == '-t':
			try:
				timeout = float(arg)
			except ValueError:
				usage()

	print( __version__ )
	for r in DVRIPClient.discover(interface, timeout):
		print( f'Serial:   {r.serial}\nMAC:      {r.mac}\nName:     {r.name}\nHost:     {r.host}/{r.mask}\nVia:      {r.router}\nPort      {r.tcpport}\nChannels: {r.channels}' )


def main() -> None:
	from sys import argv
	from dvrip.cmd import host

	if host() is not None:
		usage()

	guard(run, argv[1:])
