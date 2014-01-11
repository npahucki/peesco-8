#!/usr/bin/env python

from bartendro import app
import logging
import os
import memcache
import sys
import serial
from bartendro.router import driver
from bartendro import mixer
from bartendro.errors import SerialIOError, I2CIOError
from indio import indio, pololu


def print_software_only_notice():
    print """If you're trying to run this code without having Bartendro hardware,
you can still run the software portion of it in a simulation mode. In this mode no 
communication with the Bartendro hardware will happen to allow the software to run.
To enable this mode, set the BARTENDRO_SOFTWARE_ONLY environment variable to 1 and 
try again:

    > export BARTENDRO_SOFTWARE_ONLY=1

"""

try:
    import config
except ImportError:
    print "You need to create a configuration file called config.py by copying"
    print "config.py.default to config.py . Edit the configuration options in that"
    print "file to tune bartendro to your needs, then start the server again."
    sys.exit(-1)
app.options = config

if len(sys.argv) > 1 and sys.argv[1] == "--debug":
    debug = True
else:
    debug = False

try: 
    app.software_only = int(os.environ['BARTENDRO_SOFTWARE_ONLY'])
    app.num_dispensers = 8
except KeyError:
    app.software_only = 0

if not os.path.exists("bartendro.db"):
    print "bartendro.db file not found. Please copy bartendro.db.default to "
    print "bartendro.db in order to provide Bartendro with a starting database."
    sys.exit(-1)

# Create a memcache connection and flush everything
app.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
app.mc.flush_all()

app.log = logging.getLogger('bartendro')

# Config indio
try:
    if app.software_only:
        ser=sys.stdout
    else:
        ser=serial.Serial('/dev/ttyACM0', 56000, timeout=1)
    pol= pololu.Pololu(ser)
    app.indios = [None] * 8
    app.indios[0] = indio.Indio(pol,0,0)
    app.indios[1] = indio.Indio(pol,0,1)
    app.indios[2] = indio.Indio(pol,0,2)
    app.indios[3] = indio.Indio(pol,0,3) 
    app.indios[4] = indio.Indio(pol,1,0)
    app.indios[5] = indio.Indio(pol,1,1)
    app.indios[6] = indio.Indio(pol,1,2)
    app.indios[7] = indio.Indio(pol,1,3,20) # This guy aims a little too high
    for indio in app.indios:
        indio.sit()
        indio.center()
except RuntimeError as e:
    print
    print "Cannot configure Indios:{0} - {1}".format(e.errno, e.strerror)
    print
    sys.exit(-1)


try:
    app.driver = driver.RouterDriver("/dev/ttyAMA0", app.software_only);
    app.driver.open()
except I2CIOError:
    print
    print "Cannot open I2C interface to a router board."
    print
    print_software_only_notice()
    sys.exit(-1)
except SerialIOError:
    print
    print "Cannot open serial interface to a router board."
    print
    print_software_only_notice()
    sys.exit(-1)

if app.software_only:
    app.log.info("Running SOFTWARE ONLY VERSION. No communication between software and hardware chain will happen!")

app.log.info("Found %d dispensers." % app.driver.count())

app.mixer = mixer.Mixer(app.driver, app.mc)

app.log.info("Bartendro starting")

app.debug = debug
app.run(host='127.0.0.1', port=8080)
