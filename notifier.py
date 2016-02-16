#!/usr/bin/python
from __future__ import print_function
import yaml
import sys
import twilio
from twilio.rest import TwilioRestClient 
import psutil
 
CONFIG_FILE = "config.yml"

# read configuration files
def get_config(file):
	try:
		config = yaml.safe_load(open(file))
		return config
	except IOError:
		print("> Error loading configuration file. Make sure that " + CONFIG_FILE + " exists and try again.", file=sys.stderr)
		exit(1)

# send text via Twilio
def send_message(config, data):
	ACCOUNT_SID = config['sid'] 
	AUTH_TOKEN = config['secret']

	try: 
		client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
		message = client.messages.create(
			to="+" + str(config['to']), 
			from_="+" + str(config['from']), 
			body=data
		)
	except twilio.TwilioRestException as e:
		print('> Error sending text notification: ' + str(e), file=sys.stderr)
		return 0
	return 1

if __name__ == '__main__':
	if (len(sys.argv) != 2):
		print('> Usage: notifier.py <pid>')
		exit(1)
	
	pid = 0
	name = ''
	try:
		pid = int(sys.argv[1])
		process = psutil.Process(pid)
		name = process.name()
	except psutil.NoSuchProcess as e:
		print('> PID: ' + str(pid) + ' does not exist')
		exit(1)
	except ValueError as e:
		print('> PID is incorrect')
		exit(1)

	config = get_config(CONFIG_FILE)
	print('> Monitoring ' + name )
	
	while(psutil.pid_exists(pid)):
		pass

	print('> Process ended')
	if(send_message(config, "Process notifier: \nProcess " + name + " ended.")):
		print("> Message sent")
	exit(0)
