#!/usr/bin/env python

from SimpleHTTPServer import SimpleHTTPRequestHandler
import BaseHTTPServer
import SocketServer
import json
import urlparse
import requests

class S(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def _set_headers(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        parsed_path = urlparse.urlparse(self.path)
        print parsed_path
        requested_term = parsed_path.query
        response = self.getTimeseriesData(requested_term)
        self.wfile.write(response)

    def do_HEAD(self):
        self._set_headers()

    def getTimeseriesData(self, term):
        r = requests.get('https://www.google.com/trends/fetchComponent?hl=en-US&q=' + term + '&cid=TIMESERIES_GRAPH_0&export=3&w=500&h=300')
        stripped = r.content[r.content.index('{') : r.content.rindex('}')]
        return stripped

    def getGeoData(self, term):
        r = requests.get('https://www.google.com/trends/api/widgetdata/comparedgeo/csv?req=%7B%22geo%22%3A%7B%7D%2C%22comparisonItem%22%3A%5B%7B%22time%22%3A%222011-12-03%202016-12-03%22%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22' + term + '%22%7D%5D%7D%7D%5D%2C%22resolution%22%3A%22COUNTRY%22%2C%22locale%22%3A%22en-US%22%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22IZG%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAWESAvd4dZTl8n9BzAouebeW12mzknd18&tz=300')
        return r.content

def run(server_class=BaseHTTPServer.HTTPServer, handler_class=S, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
