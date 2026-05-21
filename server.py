#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import argparse
import socket


class Handler(BaseHTTPRequestHandler):
    server_version = "SimpleHomeworkHTTP/1.0"

    def do_GET(self):
        body = (
            f"server={self.server.server_name_label}\n"
            f"host={socket.gethostname()}\n"
            f"port={self.server.server_port}\n"
            f"path={self.path}\n"
        ).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"{self.server.server_name_label}: {self.address_string()} - {fmt % args}")


def main():
    parser = argparse.ArgumentParser(description="Simple HTTP server for HAProxy homework")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    httpd = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    httpd.server_name_label = args.name
    print(f"Starting {args.name} on 127.0.0.1:{args.port}")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
