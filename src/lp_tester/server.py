from gevent import monkey
monkey.patch_all()

import random
import time

from gevent import Greenlet, pywsgi, queue


HOST = '0.0.0.0'
PORT = 80


def current_time(body):
    for counter in xrange(random.randint(1, 50)):
        body.put(str(counter) + '\n')
        time.sleep(1)

    body.put(StopIteration)


def handle(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    body = queue.Queue()
    Greenlet.spawn(current_time, body)
    return body


def main():
    server = pywsgi.WSGIServer\
        ( (HOST, PORT)
        , handle
        )
    print "Serving on http://%s:%s ..." % (HOST, PORT)
    server.serve_forever()


if __name__ == '__main__':
    main()
