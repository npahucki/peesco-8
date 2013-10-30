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
indios[1] = indio.Indio(pol,0,1)
indios[2] = indio.Indio(pol,0,2)
indios[3] = indio.Indio(pol,0,3)
indios[4] = indio.Indio(pol,1,0)
indios[5] = indio.Indio(pol,1,1)
indios[6] = indio.Indio(pol,1,2)
indios[7] = indio.Indio(pol,1,3)


for indio in indios:
    indio.sit()
    indio.center()

time.sleep(.5)

for indio in indios:
    indio.stand()
    time.sleep(.5)
    indio.left()
    time.sleep(.5)
    indio.right()
    time.sleep(.5)
    indio.center()
    indio.sit()

pol.wait_done()
print "Done"
