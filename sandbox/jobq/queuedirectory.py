"""Read/write access to `QueueDir` folders. 
These folders are implemented like 'maildir' folders
so there (in theory) are no locking issues.
See http://www.qmail.org/man/man5/maildir.html

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

import os
import socket
import time
import random

class QueueDir(object):
    """An implementation of a Queue directory structure"""

    def __init__(self, path, create=False):
        """
        """
        self.path = path

        def access(path):
            return os.access(path, os.F_OK)

        subdir_cur = os.path.join(path, 'cur')
        subdir_new = os.path.join(path, 'new')
        subdir_tmp = os.path.join(path, 'tmp')

        if create and not access(path):
            os.mkdir(path)
            os.mkdir(subdir_cur)
            os.mkdir(subdir_new)
            os.mkdir(subdir_tmp)
            queuedir = True
        else:
            queuedir = (os.path.isdir(subdir_cur) and os.path.isdir(subdir_new)
                       and os.path.isdir(subdir_tmp))
        if not queuedir:
            raise ValueError('%s is not a QueueDir folder' % path)

    def __iter__(self):
        ""
        join = os.path.join
        subdir_cur = join(self.path, 'cur')
        subdir_new = join(self.path, 'new')
        new_messages = [join(subdir_new, x) for x in os.listdir(subdir_new)
                        if not x.startswith('.')]
        cur_messages = [join(subdir_cur, x) for x in os.listdir(subdir_cur)
                        if not x.startswith('.')]
        return iter(new_messages + cur_messages)

    def new_entry(self):
        ""
        join = os.path.join
        subdir_tmp = join(self.path, 'tmp')
        subdir_new = join(self.path, 'new')
        pid = os.getpid()
        host = socket.gethostname()
        randmax = 0x7fffffff
        counter = 0
        while True:
            timestamp = int(time.time())
            unique = '%d.%d.%s.%d' % (timestamp, pid, host,
                                      random.randrange(randmax))
            filename = join(subdir_tmp, unique)
            try:
                fd = os.open(filename, os.O_CREAT|os.O_EXCL|os.O_WRONLY, 0600)
            except OSError:
                # File exists
                counter += 1
                if counter >= 1000:
                    raise RuntimeError("Failed to create unique file name"
                                       " in %s, are we under a DoS attack?"
                                       % subdir_tmp)
                time.sleep(0.1)
            else:
                break
        return QueueDirEntryWriter(os.fdopen(fd, 'w'), filename,
                                    join(subdir_new, unique))


class QueueDirEntryWriter(object):
    ""

    def __init__(self, fd, filename, new_filename):
        self._filename = filename
        self._new_filename = new_filename
        self._fd = fd
        self._closed = False
        self._aborted = False

    def write(self, data):
        self._fd.write(data)

    def writelines(self, lines):
        self._fd.writelines(lines)

    def commit(self):
        if self._closed and self._aborted:
            raise RuntimeError('Cannot commit, entry already aborted')
        elif not self._closed:
            self._closed = True
            self._aborted = False
            self._fd.close()
            os.rename(self._filename, self._new_filename)
            # NOTE: the same maildir.html says it should be a link, followed by
            #       unlink.  But Win32 does not necessarily have hardlinks!

    def abort(self):
        if not self._closed:
            self._closed = True
            self._aborted = True
            self._fd.close()
            os.unlink(self._filename)


