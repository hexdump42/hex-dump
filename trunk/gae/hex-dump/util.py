# This module contains some code from Ian Bicking's WebOb 
# Do it yourself framework article
# http://pythonpaste.org/webob/do-it-yourself.html
# so is it under the following copyright and license.
#
# Copyright (c) 2007 Ian Bicking and Contributors
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import threading
class Localized(object):
    '''Keep track of an object with it's thread.
    This isn't required with GAE but just in case we
    deploy under a WSGI threaded environment.'''
    def __init__(self):
        self.local = threading.local()
    def register(self, object):
        self.local.object = object
    def unregister(self):
        del self.local.object
    def __call__(self):
        try:
            return self.local.object
        except AttributeError:
            raise TypeError("No object has been registered for this thread")

get_request = Localized()

from webob import Request

class RegisterRequest(object):
    '''Register a request'''
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        req = Request(environ)
        get_request.register(req)
        try:
            return self.app(environ, start_response)
        finally:
            get_request.unregister()

import urllib

def url(*segments, **vars):
    '''Generate an absolute url for the current application.
    
    >>> get_request.register(Request.blank('http://localhost/'))
    >>> url('article', 1)
    'http://localhost/article/1'
    >>> url('search', q='some query')
    'http://localhost/search?q=some+query'
    '''
    base_url = get_request().application_url
    path = '/'.join(str(s) for s in segments)
    if not path.startswith('/'):
        path = '/' + path
    if vars:
        path += '?' + urllib.urlencode(vars)
    return base_url + path    