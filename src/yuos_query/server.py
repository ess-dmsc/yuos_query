"""Lightweight HTTP server for on-demand proposal cache updates.

Exposes two endpoints:
  POST /reload-proposal/{proposal_id}  — re-fetch a single proposal from SciCat
  GET  /health                         — liveness check
"""

import json
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


class _Handler(BaseHTTPRequestHandler):
    """Request handler that delegates to the shared YuosServer instance."""

    yuos_server = None  # set by YuosHttpServer before starting

    def do_POST(self):
        if self.path.startswith("/reload-proposal/"):
            proposal_id = self.path.removeprefix("/reload-proposal/").strip("/")
            if not proposal_id:
                self._respond(400, {"error": "proposal_id is required"})
                return
            try:
                self.yuos_server.update_single_proposal(proposal_id)
                logging.info("reloaded proposal %s via HTTP request", proposal_id)
                self._respond(200, {"status": "ok", "proposal_id": proposal_id})
            except Exception as exc:
                logging.error("failed to reload proposal %s: %s", proposal_id, exc)
                self._respond(500, {"error": str(exc)})
        else:
            self._respond(404, {"error": "not found"})

    def do_GET(self):
        if self.path == "/health":
            self._respond(200, {"status": "ok"})
        else:
            self._respond(404, {"error": "not found"})

    def _respond(self, status: int, body: dict):
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt, *args):
        logging.debug("HTTP %s", fmt % args)


class YuosHttpServer:
    def __init__(self, yuos_server, host: str = "localhost", port: int = 14870):
        self._yuos_server = yuos_server
        self._host = host
        self._port = port
        self._thread = None

    def start(self):
        """Start the HTTP server in a background daemon thread."""

        class Handler(_Handler):
            yuos_server = self._yuos_server

        httpd = HTTPServer((self._host, self._port), Handler)
        self._thread = threading.Thread(
            target=httpd.serve_forever, name="yuos-http-server", daemon=True
        )
        self._thread.start()
        logging.info(
            "YuosHttpServer listening on %s:%d", self._host, self._port
        )
