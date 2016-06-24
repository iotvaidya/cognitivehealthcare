from gattlib import GATTRequester
import time

from gattlib import DiscoveryService

service = DiscoveryService("hci0")
devices = service.discover(2)

print "connected to ",devices.items()[0][0]

req = GATTRequester("Bluetooth MAC Adress of Peripheral")
while 1:
	name = req.read_by_uuid("2a37")[0]
	value = []
	for c in name:
		value.append(ord(c))
	if(name):
		print "Sensor value : ",value[1]

	else:
		print "*************************************"
		#time.sleep(1)
