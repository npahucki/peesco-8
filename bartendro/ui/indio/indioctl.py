#!/usr/bin/python

import sys
import time
import indio
import serial
import pololu

# Connection to the Pi serial port
ser=serial.Serial('/dev/ttyACM0', 56000, timeout=1)
pol= pololu.Pololu(ser)

indios = [None] * 8
indios[0] = indio.Indio(pol,0,0)
indios[1] = indio.Indio(pol,0,1, 80)
indios[2] = indio.Indio(pol,0,2)
indios[3] = indio.Indio(pol,0,3)
indios[4] = indio.Indio(pol,1,0)
indios[5] = indio.Indio(pol,1,1)
indios[6] = indio.Indio(pol,1,2)
indios[7] = indio.Indio(pol,1,3, 70)

cmd = sys.argv[1]   
indio = indios[int(sys.argv[2])]

if cmd == "stand":
    indio.stand()
elif cmd == "pee":
    indio.pee()
elif cmd == "sit":
    indio.sit()
elif cmd == "center":
    indio.center()
elif cmd == "left":
    indio.left()
elif cmd == "right":
    indio.right()

pol.wait_done()

time.sleep(1)        
print "Done"
