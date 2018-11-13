import serial
import os
import pynmea2
import RPi.GPIO as GPIO

gpsReset = 7
uartPort = "/dev/serial0"

os.system("systemctl disable serial-getty@ttyS0.service") # Disable getty on ttyS0

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
	
GPIO.cleanup()
