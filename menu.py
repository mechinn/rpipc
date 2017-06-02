#!/usr/bin/env python
import sys

try:
	import rpipc

	def on(name):
		rpipc.poweron(name)

	def off(name):
		rpipc.poweroff(name)

	def reset(name):
		rpipc.reset(name)

	def kill(name):
		rpipc.kill(name)

	def status(name):
		print('server {} is {}'.format(name,'on' if rpipc.status(name) else 'off'))

	actions = {
		'on': on,
		'off': off,
		'reset': reset,
		'kill': kill,
	}

	def main():
		while True:
			print("Select a server:")
			print("")
			for key in rpipc.servers.keys():
				print(key)
			print("")
			print("exit - exit program")
			server = raw_input("Server name: ")
			if server in rpipc.servers.keys():
				action_menu(server)
			elif server == "exit":
				sys.exit(0)

	def action_menu(server):
		while True:
			status(server)
			print("Take action on "+server+":")
			print("")
			for key in actions.keys():
				print(key)
			print("")
			print("exit - back to server selection")
			name = raw_input("Action name: ")
			if name in actions.keys():
				action = actions[name]
				action(server)
			elif name == "exit":
				return

	if __name__ == "__main__":
		main()

except RuntimeError:
	print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
