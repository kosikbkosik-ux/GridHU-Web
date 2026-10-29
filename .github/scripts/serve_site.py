"""Loopback-only preview with the production /GridHU-Web/ prefix and public allowlist."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlsplit
from prepare_site import ROOT, PUBLIC

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        name = unquote(urlsplit(self.path).path)
        if not name.startswith('/GridHU-Web/'):
            self.send_error(404)
            return
        name = name[len('/GridHU-Web/'):]
        if not name or name.endswith('/'):
            name += 'index.html'
        if name not in PUBLIC:
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write((ROOT / '404.html').read_bytes())
            return
        self.path = '/' + name
        super().do_GET()

if __name__ == '__main__':
    print('Preview: http://127.0.0.1:8000/GridHU-Web/ (Ctrl+C stops it)')
    ThreadingHTTPServer(('127.0.0.1', 8000), Handler).serve_forever()
