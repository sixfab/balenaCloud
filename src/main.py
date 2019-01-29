import serial
import os
import pynmea2
import RPi.GPIO as GPIO
import _thread
import rockBlock
from rockBlock import rockBlockProtocol

gpsReset = 7
uartPort = "/dev/serial0"

os.system("systemctl disable serial-getty@ttyS0.service") # Disable getty on ttyS0

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

ser = serial.Serial(uartPort, baudrate = 9600, timeout = 1)

if(ser.isOpen() == False):
	ser.open()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(gpsReset, GPIO.OUT) # Set to Low GPS Reset Pin
GPIO.output(gpsReset, 0)

print("Application Started")

while True:
	if ser.inWaiting() > 0 :
		recv=ser.readline().decode('utf-8')
	
		if recv.startswith("$GPGGA"):
			print(recv)
			msg=pynmea2.parse(recv)
			print(msg.timestamp)
			print(msg.latitude)
			print(msg.longitude)

			if( msg.timestamp.minute == 25 and msg.timestamp.second == 00):
				payload = {'timestamp': str(msg.timestamp), 'lat': msg.latitude, 'lon':msg.longitude}
				print(str(payload))
				_thread.start_new_thread( rockblock_service, (payload))
				

ser.close()
GPIO.cleanup()
