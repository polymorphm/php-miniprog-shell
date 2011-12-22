# -*- mode: python; coding: utf-8 -*-
#
# Copyright 2011 Andrej A Antonov <polymorphm@gmail.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

assert str is not bytes

import threading
import functools
import http.client, urllib.parse
import tornado.ioloop, tornado.stack_context

TIMEOUT = 7200

def http_post_request(host, path, data, use_tor=None, callback=None):
    if use_tor is None:
        use_tor = False
    
    if callback is not None:
        callback = tornado.stack_context.wrap(callback)
    
    if use_tor:
        #from blahbla import blahblahblah
        #
        #connection_factory = blahblahblah
        
        raise NotImplementedError('Tor-using not yet not implemented')
    else:
        connection_factory = http.client.HTTPConnection
    
    def daemon():
        response = None
        error = None
        
        try:
            params = urllib.parse.urlencode(data)
            
            conn = connection_factory(host, timeout=TIMEOUT)
            conn.request('POST', path, params,
                    {'Content-type': 'application/x-www-form-urlencoded'})
            response = conn.getresponse()
        except Exception as e:
            error = e
        
        tornado.ioloop.IOLoop.instance().add_callback(
                functools.partial(callback, response, error))
    
    thread = threading.Thread(target=daemon)
    thread.daemon = True
    thread.start()
