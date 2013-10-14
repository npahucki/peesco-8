import sys
import time
import indio
import serial
import pololu
import socket
import RPi.GPIO as GPIO

POLOLU_RESET_PIN = 16

def resetPololu():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(POLOLU_RESET_PIN, GPIO.OUT)
    GPIO.output(POLOLU_RESET_PIN, GPIO.HIGH)
    time.sleep(.1)
    GPIO.output(POLOLU_RESET_PIN, GPIO.LOW)

# Connection to the Pi serial port
ser=serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
resetPololu(); # Must be AFTER Serial port is opened
pol= pololu.Pololu(ser)

#Open port and listen
#create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((socket.gethostname(), 1335))
serversocket.listen(5)

while 1: 
    client, address = serversocket.accept() 
    cmd = client.recv(size) 
    if cmd: 
        print [ord(c) for c in cmd]
        #pol.send_cmd(data) 


