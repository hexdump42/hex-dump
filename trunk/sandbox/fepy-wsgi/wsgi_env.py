def main(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    for var in sorted(environ):
        yield '%s = %s\n' % (var, environ[var])
