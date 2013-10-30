#!/usr/bin/env python

from bartendro import app
import logging
import os
import memcache
import sys
import serial
import time
from bartendro.router import driver
from bartendro import mixer
from bartendro.errors import SerialIOError, I2CIOError
from indio import indio, pololu

print "WARNING: This will activate all the pumps one at a time. Assure that there is no liquid in the tubes, OR that you are prepared to deal with liquid!"
raw_input("Press Enter to continue...")


# "Conenction to pumps
pumps = driver.RouterDriver("/dev/ttyAMA0", False);
pumps.open()

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


for idx, indio in enumerate(indios):
    indio.stand()
    time.sleep(.5)
    pumps.start(idx, 100)
    time.sleep(3)
    pumps.stop(idx)
    time.sleep(2)
    indio.dick_shake(3, True)
    time.sleep(.3)
    indio.left()
    time.sleep(.5)
    indio.right()
    time.sleep(.5)
    indio.center()
    indio.sit()

pol.wait_done()
print "Done"

