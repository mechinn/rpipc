#!/usr/bin/env python
import pprint
import argparse

try:
	import rpipc

	def poweron(name):
		status(name)
		rpipc.poweron(name)
		status(name)

	def poweroff(name):
		status(name)
		rpipc.poweroff(name)
		status(name)

	def reset(name):
		status(name)
		rpipc.reset(name)
		status(name)

	def kill(name):
		status(name)
		rpipc.kill(name)
		status(name)

	def status(name):
		print('server {} is {}'.format(name,'on' if rpipc.status(name) else 'off'))

	actions = {
		'poweron': poweron,
		'poweroff': poweroff,
		'reset': reset,
		'kill': kill,
		'status': status,
	}

	def main():
		rpipc.setup()
		try:
			parser = argparse.ArgumentParser(description='Server Power Control using a Raspberry Pi')
			parser.add_argument('--action', choices=actions.keys(), default='status', help='send what signal')
			parser.add_argument('--system', choices=rpipc.servers.keys(), nargs='*', default=rpipc.servers.keys(), help="the server(s) which to power control")
			args = parser.parse_args()
			action = actions.get(args.action)
			for system in args.system:
				action(system)
		finally:
			rpipc.close()

	if __name__ == "__main__":
		main()

except RuntimeError:
	print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
