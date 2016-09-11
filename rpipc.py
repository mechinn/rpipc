#!/usr/bin/env python3
try:
	import argparse
	from time import sleep
	import RPi.GPIO as GPIO

	GPIO.setmode(GPIO.BOARD)

	servers = [
		{
			'power': 33,
			'reset': 31,
			'powerled': 32,
			'ip': '10.4.1.40',
		},
		{
			'power': 37,
			'reset': 35,
			'powerled': 36,
			'ip': '10.4.1.41',
		},
	]
	inputs = []
	outputs = []
	for server in servers:
		inputs.append(server['powerled'])
	for server in servers:
		outputs.append(server['power'])
		outputs.append(server['reset'])
	
	def power(server):
		print('power')
		print(server)
		GPIO.output(server['power'], GPIO.LOW)
		sleep(.10)
		GPIO.output(server['power'], GPIO.HIGH)

	def reset(server):
		print('reset')
		print(server)
		GPIO.output(server['reset'], GPIO.LOW)
		sleep(.10)
		GPIO.output(server['reset'], GPIO.HIGH)

	def kill(server):
		print('kill')
		print(server)
		GPIO.output(server['power'], GPIO.LOW)
		sleep(10)
		GPIO.output(server['power'], GPIO.HIGH)

	def status(server):
		pass

	actions = {
	        'power': power,
	        'reset': reset,
	        'kill': kill,
		'status': status,
	}

	def main():
		GPIO.setup(inputs, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(outputs, GPIO.OUT, initial=GPIO.HIGH)
		try:
			parser = argparse.ArgumentParser(description='Control servers')
			parser.add_argument('action', choices=actions.keys(), nargs=1, help='send what signal')
			parser.add_argument('system', type=int, nargs='*', help='the server(s) which to power control')
			args = parser.parse_args()
			action = actions.get(args.action[0])
			if len(args.system) < 1:
				system_list = range(len(servers))
			else:
				system_list = args.system
			for system in system_list:
				server = servers[system]
				print('server {} is {}'.format(server['ip'], 'on' if GPIO.input(server['powerled']) else 'off'))
				action(server)
		finally:
			GPIO.cleanup()

	if __name__ == "__main__":
		main()

except RuntimeError:
	print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
