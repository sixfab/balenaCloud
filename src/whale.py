import serial
import os
import pynmea2
import RPi.GPIO as GPIO
import _thread
import rockBlock
import time
from rockBlock import rockBlockProtocol

delay = 0
gpsLat = 0
gpsLon = 0
gpsTimestamp = 0

gpsReset = 7
uartPort = "/dev/serial0"

os.system("systemctl disable serial-getty@ttyS0.service") # Disable getty on ttyS0

push_interval = int(os.getenv('PUSH_INTERVAL', 0))

class RockBlockClient (rockBlockProtocol):
    
    def send(self, msg):
      
        rb = rockBlock.rockBlock("/dev/ttyUSB0", self)
        
        rb.sendMessage(msg)      
        
        rb.close()
        
    def rockBlockTxStarted(self):
        print ("rockBlockTxStarted")
        
    def rockBlockTxFailed(self):
        print ("rockBlockTxFailed")
        
    def rockBlockTxSuccess(self,momsn):
        print ("rockBlockTxSuccess " + str(momsn))

def rockblock_service(payload):
	print("RockBlock Thread Started...")
	RockBlockClient().send(str(payload))
	print("RockBlock Thread Finished...")


def sendToServer():
	payload = {'timestamp': str(gpsTimestamp), 'lat': gpsLat, 'lon':gpsLon}
	print(str(payload))
	_thread.start_new_thread( rockblock_service, (payload,))


now = int(time.time())

if push_interval == 0:
	print("Please set PUSH_INTERVAL env variable")
	exit()
else:
	print("PUSH_INTERVAL :" , push_interval)

if push_interval == 1:
	delay = 6*60*60 # 6 hour second

elif push_interval == 2:
	delay = 1*60*60 # 1 hour second

elif push_interval == 3:
	delay = 30*60 # 30 Minute second

elif push_interval == 4:
	delay = 15*60 # 15 Minute second

elif push_interval == 5: # Every 15 minute UTC
	targetMinute = 15

elif push_interval == 6: # Every 30 minute UTC
	targetMinute = 30

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(gpsReset, GPIO.OUT) # Set to Low GPS Reset Pin
GPIO.output(gpsReset, 0)

ser = serial.Serial(uartPort, baudrate = 9600, timeout = 1)
if(ser.isOpen() == False):
	ser.open()

print("Application Started")

while True:
	if ser.inWaiting() > 0 :
		recv=ser.readline().decode('utf-8')
	
		if recv.startswith("$GPGGA"):
			#print(recv)
			msg=pynmea2.parse(recv)

			if( msg.gps_qual ): #GPS Fixed Quality OK

				gpsLat = msg.latitude
				gpsLon = msg.longitude
				gpsTimestamp = msg.timestamp


	if push_interval >=1 and push_interval <= 4:
		
		if int(time.time()) >= now + delay:

			now = int(time.time())

			sendToServer()

	elif push_interval >=5 and  push_interval <= 6:

		if( ( ( gpsTimestamp.minute % targetMinute ) == 0 )  and gpsTimestamp.second == 0):

			sendToServer()

	elif push_interval == 7:

		if( ( gpsTimestamp.minute == 0 )  and gpsTimestamp.second == 0 ):
			
			sendToServer()


ser.close()
GPIO.cleanup()
