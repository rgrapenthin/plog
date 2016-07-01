# plog
static python logging class that can be turned on / off

### Overview
I use this in a number of projects; it's multiprocessing safe (i.e., 
the multiple processes don't write at the same time to create
wonderful gibberish). There are certainly other classes that do 
this job, but this is the one I clobbered together over the years. Thanks.

### Test
I include the following test (`plog_test.py`); its output is given at the 
bottom. Note that `Logger.debug(...)` will not give any output when run 
via `python -O` (that's a feature!):

```
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
```

### Output
```
[ Debug ] Debug Message
 
Info Message
 
[ WARNING ] Warning Message (no trace included)
 
------------------------------------------------------------
Traceback (most recent call last):
  File "./plog_test.py", line 12, in <module>
    x=x
NameError: name 'x' is not defined
------------------------------------------------------------
[ WARNING ] Warning Message (trace included)
 
 

################################################################################
[ SERIOUS WARNING ] Serious Warning
################################################################################
 
------------------------------------------------------------
Traceback (most recent call last):
  File "./plog_test.py", line 12, in <module>
    x=x
NameError: name 'x' is not defined
------------------------------------------------------------

################################################################################
[ SERIOUS WARNING ] Serious Warning with trace
################################################################################
 
[ Debug ] Debug-Test (Logger On)
 
Info-Test (Logger On)
 
>>>>> [ ERROR ] ugh. 
------------------------------------------------------------
  File "./plog_test.py", line 39, in <module>
    Logger.error("ugh.", 23)
  File "/usr/local/plog/plog.py", line 84, in error
    traceback.print_stack(file=out)
------------------------------------------------------------
[ ERROR ] Aborting. 
initiating cleanup
```
