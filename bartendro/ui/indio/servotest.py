import serial
import sys
ser=serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

def setpos(n,angle):
  #Quick check that things are in range
  if angle > 180 or angle <0:
    angle=90
    print "WARNING: Angle range should be between 0 and 180. Setting angle to 90 degrees to be safe..."
    print "moving servo "+str(n)+" to "+str(angle)+" degrees."

  byteone=int(254*angle/180)
  #move to an absolute position in 8-bit mode (0x04 for the mode, 0 for the servo, 0-255 for the position (spread over two bytes))
  bud=chr(0xFF)+chr(n)+chr(byteone)
  ser.write(bud)

n=int(sys.argv[1])
m=int(sys.argv[2])
setpos(n,m)
ser.close()
