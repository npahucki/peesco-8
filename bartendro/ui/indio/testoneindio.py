import sys
import time
import indio
import serial
import pololu

# Connection to the Pi serial port
ser=serial.Serial('/dev/cu.usbmodem00059921', 56000, timeout=1)
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
    indio1.center(50)
    time.sleep(.5)
    indio1.center()
    time.sleep(.5)
    
indio1.center()
time.sleep(.5)

indio1.stand(0,0,60)
time.sleep(2)

for x in range(0,3):
    indio1.center(50,30)
    time.sleep(.75);
    indio1.center(-50,30)
    time.sleep(.75)		

indio1.center()

indio1.dick_shake(5, True)
indio1.side_shake(3, True)

indio1.sit()
indio1.center()

pol.wait_done()
print "Done"
