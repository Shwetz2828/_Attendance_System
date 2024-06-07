# Importing required modules
import http.server  # Module for creating HTTP servers
import socketserver  # Module for creating network servers

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
