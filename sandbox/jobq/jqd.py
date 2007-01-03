"""Job Queue Daemon 

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
__docformat__ = 'restructuredtext'

import threading
import os
from queueprocessor import QueueProcessorThread
from configobj import ConfigObj
from subprocess import Popen

def create_fileobj(filename, mode='w'):
    """
    Create a file object from a valid filename,
    otherwise return None.
    """
    if filename is not None:
        return open(filename, mode)
    else:
        return None
    
def create_envdict(filename):
    """
    Create an environment dictionary using the contents from 
    a valid filename, otherwise return None.
    """
    environ = {}
    if filename is not None:
        f = open(filename, "r")
        for line in f.readlines():
            line = line.replace(os.linesep,'')
            key, value = line.split('=')
            environ[key] = value
        return environ
    else:
        return None
    
class JobQueueProcessor(QueueProcessorThread):
    def __init__(self, name, poll_wait=3):
        QueueProcessorThread.__init__(self, name, poll_wait)
        
    def set_queue_path(self, path):
        QueueProcessorThread.set_queue_path(self, path)
        # If required, create directories for completed 
        # and failed processed jobs
        self.subdir_ok = os.path.join(path, 'ok-done')
        self.subdir_fail = os.path.join(path, 'fail-done')
        try:
                os.mkdir(self.subdir_ok)
                os.mkdir(self.subdir_fail)
        except:
            pass
     
    def _parse_entry(self, entry, jobid):
        """
        Parse the entry into a ConfigObj.
        """        
        cfg = ConfigObj(entry)
        cfg['jobid'] = jobid
        if not cfg.has_key('job_name'):
            cfg['job_name'] = jobid
        return cfg
     
    def _process_entry(self, entry):
        """
        Process the job command ConfigObj.
        """
        self.log.debug(entry)
        self.log.info("Processing job %s" % entry['job_name'])
        executable = entry.get('executable',None)
        args = entry.get('arguments','')
        input = create_fileobj(entry.get('input', None))
        output = create_fileobj(entry.get('output', None))
        error = create_fileobj(entry.get('error', None))
        environ = create_envdict(entry.get('env', None))
        cwd = entry.get('cwd', None)
        try:
            retcode = Popen(args, 
                    bufsize=0, executable=executable, 
                    stdin=input, stdout=output, stderr=error, 
                    preexec_fn=None, close_fds=False, 
                    shell=False, cwd=cwd, env=environ, 
                    universal_newlines=False, 
                    startupinfo=None, creationflags=0)
        except Exception, e:
            self.log.error("Error processing jobid %s:%s" % (entry['jobid'], e))
            if error is not None:
                error = create_fileobj(entry.get('error', None),'a')
                error.write(str(e))
                error.close()
            retcode = -1
        if retcode == 0:
            return True
        else:
            return False
           
    def _unlink(self, status, filename):
        """
        Dependant of return status of executed process, copy job command file
        to either ok or fail directory.
        """
        if status:
            new_filename = os.path.join(self.subdir_ok, 
                                        os.path.basename(filename))
        else:
            new_filename = os.path.join(self.subdir_fail, 
                                        os.path.basename(filename))
        os.rename(filename, new_filename)
        
if __name__ == '__main__':
    print "Setup and start JobQ 1..."
    jq = JobQueueProcessor("jq1")
    jq.set_queue_path("/tmp/jq")
    jq.start()
    print "Setup and start JobQ 2..."
    jq2 = JobQueueProcessor("jq2",5)
    jq2.set_queue_path("/tmp/jq2")
    jq2.start()
    
