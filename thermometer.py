#!/usr/bin/python

'''
Gene Blanchard

Use a digital thermometer
'''
#from beer import GPIO
import glob
import os
import time

# Digital thermoprobe
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines
 
def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return "%.1f" % temp_f

def read_status():
	thermostat_status = open('/sys/class/gpio/gpio23/value', 'r').readline()
	if thermostat_status.rstrip() == '1':
		thermostat_int = 1
	if thermostat_status.rstrip() == '0':
		thermostat_int = 0
	return thermostat_int
