#!/usr/bin/env python
#
# Copyright 2008 Mark Rees (http://hex-dump.blogspot.com)
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

from docutils.core import publish_string as rst_render
from docutils import core
from docutils.writers.html4css1 import Writer,HTMLTranslator

class NoHeaderHTMLTranslator(HTMLTranslator):
    def astext(self):
        return ''.join(self.body)

_w = Writer()
_w.translator_class = NoHeaderHTMLTranslator


class Rest2Html(object):
    def __init__(self, req):
        self.request = req
    def get(self):
        if self.request.params.get('text', False):
            return self._render(self.request.params['text'])
        else:
            return """<form method="POST">
            Enter <a href="http://docutils.sourceforge.net/rst.html" >reStructured Text:</a><br><textarea rows="10" cols="60" name="text"></textarea>
            <br><input type="submit" value="Convert to HTML">
            </form>
            <a href='%s'>Home</a>
            """ % (url(),)
    def post(self):
        text = self.request.params['text']
        return self._render(text)
    def _render(self, text):
        logging.info(text)
        return rst_render(text, writer=_w)
        
rst2html = rest_controller(Rest2Html)
rst2html = RegisterRequest(rst2html)
            
def main():
  application = Router()
  application.add_route('/', controller=rst2html)
                            
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
