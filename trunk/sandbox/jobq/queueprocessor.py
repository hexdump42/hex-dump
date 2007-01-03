"""Threaded Queue Processor

License: MIT

Copyright (c) 2006-2007 Mark J. Rees

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.

$Id$
"""
import threading
import logging
from os import unlink, path
import atexit
import time
from queuedirectory import QueueDir

class QueueProcessorThread(threading.Thread):
    ""

    log = logging.getLogger("QueueProcessorThread")
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')
    __stopped = False

    def __init__(self, name, poll_pause=3):
        threading.Thread.__init__(self)
        self.name = name
        self.poll_pause = poll_pause
        self.queue_dir = None
        self.__stopped = False

    def set_queue_path(self, path):
        self.queue_dir = QueueDir(path, True)

    def _parse_entry(self, entry, jobid):
        """
        Abstract method
        """
        return entry
     
    def _process_entry(self, entry):
        """
        Abstract method
        """
        return True  
    
    def _unlink(self, status, filename):
        if status:
            unlink(filename) 

    def run(self, forever=True):
        atexit.register(self.stop)
        while not self.__stopped:
            self.log.info("Check queue directories for %s..." % self.name)
            for filename in self.queue_dir:
                try:
                    self.log.info("Processing entry %s.",
                                  filename)
                    file = open(filename)
                    entry = file.readlines()
                    file.close()
                    entry = self._parse_entry(entry, path.basename(filename))
                    retstat = self._process_entry(entry)
                    self._unlink(retstat, filename)
                except:
                    self.log.error(
                        "Error while processing job command file : %s ",
                        filename, exc_info=True)
            else:
                if forever:
                    time.sleep(self.poll_pause)

            if not forever:
                break

    def stop(self):
        self.__stopped = True
