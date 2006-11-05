"""
Written by Marc-Andre Lemburg (mal@lemburg.com).

Modified by Christopher Baus (christopher@baus.net)

I included part of pypy's _codecs implementation which
registers the error handles.  This seems to be missing
from IronPython.  By including this in site.py, codecs
seems to work correctly.


Copyright (c) Corporation for National Research Initiatives.

"""
import _codecs

def strict_errors(exc):
    if isinstance(exc,Exception):
        raise exc
    else:
        raise TypeError("codec must pass exception instance")
    
def ignore_errors(exc):
    if isinstance(exc,(UnicodeEncodeError,UnicodeDecodeError,UnicodeTranslateError)):
        return u'',exc.end
    else:
        raise TypeError("don't know how to handle %.400s in error callback"%exc)

Py_UNICODE_REPLACEMENT_CHARACTER = u"\ufffd"

def replace_errors(exc):
    if isinstance(exc,UnicodeEncodeError):
        return u'?'*(exc.end-exc.start),exc.end
    elif isinstance(exc,(UnicodeTranslateError,UnicodeDecodeError)):
        return Py_UNICODE_REPLACEMENT_CHARACTER*(exc.end-exc.start),exc.end
    else:
        raise TypeError("don't know how to handle %.400s in error callback"%exc)

def xmlcharrefreplace_errors(exc):
    if isinstance(exc,UnicodeEncodeError):
        res = []
        for ch in exc.object[exc.start:exc.end]:
            res += '&#'
            res += str(ord(ch))
            res += ';'
        return u''.join(res),exc.end
    else:
        raise TypeError("don't know how to handle %.400s in error callback"%type(exc))
    
def backslashreplace_errors(exc):
    if isinstance(exc,UnicodeEncodeError):
        p=[]
        for c in exc.object[exc.start:exc.end]:
            p.append('\\')
            oc = ord(c)
            if (oc >= 0x00010000):
                p.append('U')
                p.append("%.8x" % ord(c))
            elif (oc >= 0x100):
                p.append('u')
                p.append("%.4x" % ord(c))
            else:
                p.append('x')
                p.append("%.2x" % ord(c))
        return u''.join(p),exc.end
    else:
        raise TypeError("don't know how to handle %.400s in error callback"%type(exc))

_codecs.register_error("strict",strict_errors)
_codecs.register_error("ignore",ignore_errors)
_codecs.register_error("replace",replace_errors)
_codecs.register_error("xmlcharrefreplace",xmlcharrefreplace_errors)
_codecs.register_error("backslashreplace",backslashreplace_errors)
