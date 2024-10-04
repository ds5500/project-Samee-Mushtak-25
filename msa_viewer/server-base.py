from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import socketserver

PORT = 8080

with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
