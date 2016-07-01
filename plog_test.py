#!/usr/bin/env python

from plog import *

Logger.debug("Debug Message")
print " "

Logger.info("Info Message")
print " "

try:
	x=x
except:
	Logger.warning("Warning Message (no trace included)")
        print " "
	Logger.warning("Warning Message (trace included)", trace=True)
	print " "

print " "
Logger.serious_warning("Serious Warning")
print " "
Logger.serious_warning("Serious Warning with trace", trace=True)

#Turn off the logger for a section in the code and all output 
#is hidden (sent to /dev/null, really)
Logger.off()
Logger.debug("Debug-Test (Logger Off)")
Logger.info("Info-Test (Logger Off)")

#Turn it back on to see the messages in other parts of the code
Logger.on()
print " "
Logger.debug("Debug-Test (Logger On)")
print " "
Logger.info("Info-Test (Logger On)")
print " "

try:
	Logger.error("ugh.", 23)
except CleanShutdownRequest:
	print "initiating cleanup"






