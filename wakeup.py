"""
Wake Light for Blinky Tape and Sense HAT

To run on default (Raspberry Pi) USB serial port: python wakeup.py &
Use cron to run at the correct time 
e.g. to run at 06:15 every weekday run crontab -e and add
15 6 * * 1-5 python /home/pi/pi-glowbe/wakeup.py

(C) 2016 James Singleton (https://unop.uk)
MIT Licensed

"""

from BlinkyTape import BlinkyTape
from sense_hat import SenseHat
from time import sleep
import optparse

# Default Blinky Tape port on Raspberry Pi is /dev/ttyACM0
parser = optparse.OptionParser()
parser.add_option("-p", "--port", dest="portname",
                  help="serial port (ex: /dev/ttyACM0)", default="/dev/ttyACM0")
(options, args) = parser.parse_args()

if options.portname is not None:
    port = options.portname
else:
    print "Usage: python wakeup.py -p <port name>"
    print "(ex.: python wakeup.py -p /dev/ttyACM0)"
    exit()

sense = SenseHat()
bt = BlinkyTape(port)


# wake phase - gradually get brighter, linearly

sleepTime = 18 # 18 sec for 30 min in 100 steps
maxPower = 100 # flickers or cuts out above 100

for y in xrange(maxPower):
    sense.clear(y * 2, y * 2, y * 2)
    for x in xrange(sleepTime):
        bt.displayColor(y, y, y)
        sleep(1)


# on phase - at full brightness for the same time

sense.clear(255, 255, 255)
for z in xrange(maxPower * sleepTime):
    bt.displayColor(maxPower, maxPower, maxPower)
    sleep(1)


# tidy up

sense.clear()
