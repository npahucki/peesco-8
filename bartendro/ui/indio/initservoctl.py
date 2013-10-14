#!/usr/bin/python
import serial
import sys
import time

ser=serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
print "Rest controller now..."
time.sleep(2)
ser.write(chr(255))
