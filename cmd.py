#!/usr/bin/env python
import pprint
import argparse

try:
	import rpipc

	def rpipc_action(name,fun):
		status(name)
		fun(name)
		status(name)

	def poweron(name):
		rpipc_action(name,rpipc.poweron)

	def poweroff(name):
		rpipc_action(name,rpipc.poweroff)

	def reset(name):
		rpipc_action(name,rpipc.reset)

	def kill(name):
		rpipc_action(name,rpipc.kill)

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
		parser = argparse.ArgumentParser(description='Server Power Control using a Raspberry Pi')
		parser.add_argument('--action', choices=actions.keys(), default='status', help='send what signal')
		parser.add_argument('--system', choices=rpipc.servers.keys(), nargs='*', default=rpipc.servers.keys(), help="the server(s) which to power control")
		args = parser.parse_args()
		action = actions.get(args.action)
		for system in args.system:
			action(system)

	if __name__ == "__main__":
		main()

except RuntimeError:
	print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
