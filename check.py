import os
import re
import subprocess

class AmonChecker(object):

	def __init__(self):
		pass


	def get__memory_info(self):
		
		regex = re.compile(r'([0-9]+)')

		mem_dict = {}
		
		with open('/proc/meminfo', 'r') as lines:
			for line in lines:
				values = line.split(':')	
				
				match = re.search(regex, values[1])
				mem_dict[values[0]] = int(match.group(0)) / 1024
			return mem_dict


	def get_disk_usage(self):
		df = subprocess.Popen(['df','-h'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]	
		
		volumes = df.split('\n')	
		volumes.pop(0)	# remove the header
		volumes.pop()

		data = {}


		for volume in volumes:
			line = volume.split()
			if line[0].startswith('/'):
				data[line[0]] = line[1:]	

		return data
				
		
	def get_uptime(self):

		with open('/proc/uptime', 'r') as line:
			contents = line.read().split()
 
		total_seconds = float(contents[0])
 
		MINUTE  = 60
		HOUR    = MINUTE * 60
		DAY     = HOUR * 24

		days    = int( total_seconds / DAY )
		hours   = int( ( total_seconds % DAY ) / HOUR )
		minutes = int( ( total_seconds % HOUR ) / MINUTE )
		seconds = int( total_seconds % MINUTE )
	 
		uptime = "{0} days {1} hours {2} minutes {3} seconds".format(days, hours, minutes, seconds)

		return uptime



	def get_network_traffic(self):
		
		lines = open("/proc/net/dev", "r").readlines()

		columnLine = lines[1]
		_, receiveCols , transmitCols = columnLine.split("|")
		receiveCols = map(lambda a:"recv_"+a, receiveCols.split())
		transmitCols = map(lambda a:"trans_"+a, transmitCols.split())

		cols = receiveCols+transmitCols

		faces = {}

		for line in lines[2:]:
			if line.find(":") < 0: continue
			face, data = line.split(":")
			faceData = dict(zip(cols, data.split()))
			faces[face] = faceData

		return faces


	def get_load_average(self):
		lines = open('/proc/loadavg','r').readlines()

		load = lines[0].split()

		return load
		
	def get_cpu_utilization(self):
		vmstat = subprocess.Popen(['vmstat'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]	
		
		lines = vmstat.splitlines()
		raw_data = lines[2].split()
		cpu_dict = raw_data[-4:]

		return cpu_dict
		



	# WORK IN PROGRESS
	def _pid_list(self):
		return [int(x) for x in os.listdir('/proc') if x.isdigit()] 



