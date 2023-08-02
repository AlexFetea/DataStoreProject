from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

class Node:
    def __init__(self, id, port, nodes):
        self.id = id
        self.port = port
        self.nodes = nodes
        self.data = {}

    def add(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def delete(self, key):
        if key in self.data:
            del self.data[key]

    def handler(self):
        node = self
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                key = parse_qs(urlparse(self.path).query).get('key')
                if key:
                    value = node.get(key[0])
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(bytes(str(value), "utf-8"))
                else:
                    self.send_response(400)
                    self.end_headers()
            def do_POST(self):
                length = int(self.headers.get('content-length'))
                field_data = self.rfile.read(length)
                fields = parse_qs(field_data)
                key = fields.get(b'key')
                value = fields.get(b'value')
                if key and value:
                    node.add(key[0].decode(), value[0].decode())
                    self.send_response(200)
                    self.end_headers()
                else:
                    self.send_response(400)
                    self.end_headers()
            def do_DELETE(self):
                key = parse_qs(urlparse(self.path).query).get('key')
                if key:
                    node.delete(key[0])
                    self.send_response(200)
                    self.end_headers()
                else:
                    self.send_response(400)
                    self.end_headers()
        return Handler

    def run(self):
        server = HTTPServer(('localhost', self.port), self.handler())
        server.serve_forever()