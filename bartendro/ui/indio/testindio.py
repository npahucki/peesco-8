import sys
import time
import indio
import serial
import pololu

# Connection to the Pi serial port
ser=serial.Serial('/dev/ttyACM0', 56000, timeout=1)
#ser=sys.stdout # for debugging
pol= pololu.Pololu(ser)

indio1 = indio.Indio(pol,0,0)
indio1.sit()
indio1.center()


indio1.sit(50)
time.sleep(.5)
indio1.sit();
time.sleep(.5)
indio1.sit(50)
time.sleep(.5)
indio1.sit();
time.sleep(.5)
indio1.sit(50)
time.sleep(.5)
indio1.sit();
time.sleep(.5)

for x in range(0,1):
    indio1.center(-50)
    time.sleep(.5)
    indio1.center()
    time.sleep(.5)
    indio1.center(-50)
indio1.center()

indio1.stand(0,30)
time.sleep(.3)

for x in range(0,3):
    indio1.center(50,15)
    time.sleep(.75);
    indio1.center(-50,15)
    time.sleep(.75)		

indio1.center()

indio1.dick_shake(5, True)

indio1.side_shake(3, False)

indio1.sit()

pol.wait_done()
print "Done"
