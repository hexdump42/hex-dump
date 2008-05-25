#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging
import wsgiref.handlers

from router import Router, controller, rest_controller
from util import RegisterRequest, url, get_request

@controller
def welcome(req):
    if req.method == 'GET':
        return """
        <html>
        <body>
        <h1><a href='http://hex-dump.blogspot.com'>My</a> <a
                href='http://code.google.com/appengine/'>Google App Engine<a> playground</h1>
            <p>The examples on this site uses a python web framework based on Ian Bickings' 
            <a href='http://pythonpaste.org/webob/do-it-yourself.html'>"Another do it yourself framework"</a> article.
            <ul>
                <li><a href='%s'>The standard "hello world" demo</a></li>
            </ul>
            <ul>
                <li><a href='%s'>Convert ReStructured Text to html</a></li>
            </ul>
        </body>
        </html>
        """ % (url('hello'), url('rst2html'))
        
welcome = RegisterRequest(welcome)            

class Hello(object):
    def __init__(self, req):
        self.request = req
    def get(self):
        return """<form method="POST">
        You're name: <input type="text" name="name">
        <input type="submit">
        </form>
        <a href='%s'>Home</a>
        """ % (url(),)
    def post(self):
        return 'Hello %s!' % self.request.params['name']

hello = rest_controller(Hello)
hello = RegisterRequest(hello)
            
def main():
  application = Router()
  application.add_route('/', controller=welcome)
  application.add_route('/hello', controller=hello)
  from rst2html import rst2html
  application.add_route('/rst2html', controller=rst2html)
                            
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
