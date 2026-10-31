"""Loopback-only preview of the custom-domain root and explicit public allowlist."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlsplit
from prepare_site import ROOT, PUBLIC

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def route_public(self, head_only=False):
        request = urlsplit(self.path)
        name = unquote(request.path).removeprefix('/')
        if not name or name.endswith('/'):
            name += 'index.html'
        elif name + '/index.html' in PUBLIC:
            self.send_response(301)
            self.send_header('Location', request.path + '/' +
                             ('?' + request.query if request.query else ''))
            self.send_header('Content-Length', '0')
            self.end_headers()
            return False
        if name not in PUBLIC:
            body = (ROOT / '404.html').read_bytes()
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            if not head_only:
                self.wfile.write(body)
            return False
        self.path = '/' + name
        return True

    def do_GET(self):
        if self.route_public():
            super().do_GET()

    def do_HEAD(self):
        if self.route_public(head_only=True):
            super().do_HEAD()

if __name__ == '__main__':
    print('Preview: http://127.0.0.1:8000/ (Ctrl+C stops it)')
    ThreadingHTTPServer(('127.0.0.1', 8000), Handler).serve_forever()
