from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import socketserver

PORT = 8080

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = '/msa_viewer.html'
        try:
            header = open('msa_viewer_header.html').read()
            footer = open('msa_viewer_footer.html').read()

            # alignment = open('alignments/pyrococcus-furiosus-aligned.fasta').read()
            alignment = open('alignments/pyrococcus-furiosus.clustal').read()
            align_js = '\\n\\\n'.join(alignment.split('\n'))
            template = f'var fasta = "{align_js}";'

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(bytes(header, 'utf-8'))
            self.wfile.write(bytes(template, 'utf-8'))
            self.wfile.write(bytes(footer, 'utf-8'))
        except:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
