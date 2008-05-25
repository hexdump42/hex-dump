# This module is based on Ian Bicking's WebOb Do it yourself framework article
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

import re
var_regex = re.compile(r'\{(\w+)(?::([^}]+))?\}', re.VERBOSE)

def template_to_regex(template):
    regex = ''
    last_pos = 0
    for match in var_regex.finditer(template):
        regex += re.escape(template[last_pos:match.start()])
        var_name = match.group(1)
        expr = match.group(2) or '[^/]+'
        expr = '(?P<%s>%s)' % (var_name, expr)
        regex += expr
        last_pos = match.end()
    regex += re.escape(template[last_pos:])
    regex = '^%s$' % regex
    return regex

from webob import Request, Response
from webob import exc
import sys

def load_controller(string):
    module_name, func_name = string.spli(':', 1)
    __import__(module_name)
    module = sys.modules[module_name]
    func = getattr(module, func_name)
    return func
       
class Router(object):
    def __init__(self):
        self.routes = []
        
    def add_route(self, template, controller, **vars):
        if isinstance(controller, basestring):
            controller = load_controller(controller)
        self.routes.append((re.compile(template_to_regex(template)),
            controller,
            vars))
            
    def __call__(self, environ, start_response):
        req = Request(environ)
        for regex, controller, vars in self.routes:
            match = regex.match(req.path_info)
            if match:
                req.urlvars = match.groupdict()
                req.urlvars.update(vars)
                return controller(environ, start_response)
        return exc.HTTPNotFound()(environ, start_response)
    
def controller(func):
    '''Simple controller decorator
    >>> @controller
    ... def hello(req):
    ...     if req.method == 'POST':
    ...         return 'Hello %s!' % req.params['name']
    ...     elif req.method == 'GET':
    ...         return """<form method="POST">
    ...             You're name: <input type="text" name="name">
    ...             <input type="submit">
    ...             </form>"""
    >>> hello_world = Router()
    >>> hello_world.add_route('/', controller=hello)
    '''
    def replacement(environ, start_response):
        req = Request(environ)
        try:
            resp = func(req, **req.urlvars)
        except exc.HTTPException, e:
            resp = e
        if isinstance(resp, basestring):
            resp = Response(body=resp)
        return resp(environ, start_response)
    return replacement

def rest_controller(cls):
    '''Wrapper to convert class into a restful controller
    >>> class Hello(object):
    ...     def __init__(self, req):
    ...         self.request = req
    ...     def get(self):
    ...         return """<form method="POST">
    ...             You're name: <input type="text" name="name">
    ...             <input type="submit">
    ...             </form>"""
    ...     def post(self):
    ...         return 'Hello %s!' % self.request.params['name']
    >>> hello = rest_controller(Hello)
    '''
    def replacement(environ, start_response):
        req = Request(environ)
        try:
            instance = cls(req, **req.urlvars)
            action = req.urlvars.get('action')
            if action:
                action += '_' + req.method.lower()
            else:
                action = req.method.lower()
            try:
                method = getattr(instance, action)
            except AttributeError:
                raise exc.HTTPNotFound("No action %s" % action)
            resp = method()
            if isinstance(resp, basestring):
                resp = Response(body=resp)
        except exc.HTTPException, e:
            resp = e
        return resp(environ, start_response)
    return replacement    