#!/usr/bin/env python
import pprint
import os
from time import sleep
import json
import RPi.GPIO as GPIO

CLICK=3
HOLD=10

config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),'rpipc.json')

with open(config_file) as config:
	servers = json.load(config)	

GPIO.setmode(GPIO.BOARD)

inputs = []
outputs = []
for name, server in servers.iteritems():
	inputs.append(server['powerled'])
	outputs.append(server['power'])
	outputs.append(server['reset'])

def setup():
	GPIO.setup(inputs, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(outputs, GPIO.OUT, initial=GPIO.HIGH)

def close():
	GPIO.cleanup()

def _control_relay(pin, sec):
	GPIO.output(pin, GPIO.LOW)
	sleep(sec)
	GPIO.output(pin, GPIO.HIGH)

def _get_state(pin):
	return not GPIO.input(pin)

def _power(name,on,length):
	server = servers[name]
	if on != status(name):
		_control_relay(server['power'],length)

def poweron(name):
	_power(name,True,CLICK)

def poweroff(name):
	_power(name,False,CLICK)

def kill(name):
	_power(name,False,HOLD)

def reset(name):
	server = servers[name]
	_control_relay(server['reset'],CLICK)

def status(name):
	server = servers[name]
	return _get_state(server['powerled'])
