#####################################################################################
 # File:        Logger.py
 # Author:      Ronni Grapenthin, New Mexico Tech
 # Created:     2016-07-01
 # Licence:     GPL
 #
#####################################################################################
 #
 # Simple static Logger class for any python project of mine.
 # Multiprocessing-safe.
 #
 # Copyright (C) 2016-now Ronni Grapenthin
 #
 # This program is free software; you can redistribute it and/or
 # modify it under the terms of the GNU General Public License
 # as published by the Free Software Foundation; version 2
 # of the License.
 #
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # GNU General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License
 # along with this program; if not, write to the Free Software
 # Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 #
#####################################################################################

import os, sys, datetime, traceback, pprint, multiprocessing
import setup as s	
from StringIO   import StringIO

class CleanShutdownRequest(Exception):
    pass


class Logger():

    TIME_FORMAT= '%Y-%m-%dT%H:%M:%S.%fZ' # ISO 8601 standard
    
    print_lock = multiprocessing.Lock()
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', 0)
    pp         = pprint.PrettyPrinter(indent=4)
    out        = sys.stdout
    err        = sys.stderr
    devnull    = open(os.devnull, "w")

    @staticmethod
    def logTime():
        '''Defines uniform time format for log time stamp'''
        # can't use 'util' module as it includes 'Logger' module
        return datetime.datetime.utcnow().strftime(Logger.TIME_FORMAT)

    @staticmethod
    def off():
        Logger.out = Logger.devnull
        Logger.err = Logger.devnull

    @staticmethod
    def on():
        Logger.out = sys.stdout
        Logger.err = sys.stderr

    @staticmethod
    def info( msg, out=None):
        if out is None:
            out = Logger.out

        Logger.print_lock.acquire()
        out.write("%s\n" % (msg))
        Logger.print_lock.release()

    @staticmethod
    def error( msg, code, out=None ):
        if out is None:
            out = Logger.err

        Logger.print_lock.acquire()

        out.write( ">>>>> [ ERROR ] %s \n" % (msg) )
        out.write('-'*60 +"\n")
        traceback.print_stack(file=out)
        out.write('-'*60 +"\n")
        out.write( "[ ERROR ] Aborting. \n")
        Logger.print_lock.release()
        if code != 666:
            raise CleanShutdownRequest() 

    @staticmethod
    def warning( msg, out=None, trace=True ):
        if out is None:
            out = Logger.out

        Logger.print_lock.acquire()

        if trace:
            out.write('-'*60 +"\n")
            traceback.print_exc(file=out)
            out.write('-'*60 +"\n")
        
        out.write( "[ WARNING ] %s\n" % (msg) )
        Logger.print_lock.release()

    @staticmethod
    def serious_warning( msg, out=None ):
        if out is None:
            out = Logger.out

        Logger.print_lock.acquire()
        out.write( "\n"+"#"*80+"\n")
        out.write( "[ SERIOUS WARNING ] %s\n" % (msg) )
        out.write( "#"*80 + "\n")
        Logger.print_lock.release()
		
    @staticmethod
    def debug(msg, M=None, out=None):
        '''This function will print `msg' unless python is called with the -O (optimization) flag,
           which sets `__debug__' to false. This then results into a call to an empty function.'''
        if __debug__:
            if out is None:
                out = Logger.out

            Logger.print_lock.acquire()
            out.write("[ Debug ] %s\n" \
                          % (msg))

            if M is not None:
                Logger.pp.pprint(M)

            Logger.print_lock.release()

#EOF
