#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
if [ -f "$ROOT/dist/index.html" ]; then
  ROOT="$ROOT/dist"
fi
PORT=8787
OPEN_BROWSER=1
while [ "$#" -gt 0 ]; do
  case "$1" in
    --port)
      [ "$#" -ge 2 ] || { echo "Missing port number." >&2; exit 2; }
      PORT="$2"; shift 2 ;;
    --no-browser) OPEN_BROWSER=0; shift ;;
    *) echo "Usage: bash start-mac.sh [--port 8787] [--no-browser]" >&2; exit 2 ;;
  esac
done

PYTHON=""
if [ -x /usr/bin/python3 ]; then
  PYTHON=/usr/bin/python3
elif command -v python3 >/dev/null 2>&1; then
  PYTHON="$(command -v python3)"
else
  echo "Python 3 is unavailable. Install the Apple developer tools or use the Windows package on Windows." >&2
  exit 1
fi

exec "$PYTHON" - "$ROOT" "$PORT" "$OPEN_BROWSER" <<'PY'
import functools
import http.server
import pathlib
import sys
import webbrowser

root = pathlib.Path(sys.argv[1]).resolve()
port = int(sys.argv[2])
open_browser = sys.argv[3] == "1"
if not 1024 <= port <= 65535:
    raise SystemExit("The port must be between 1024 and 65535.")

class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".html": "text/html; charset=utf-8",
        ".js": "text/javascript; charset=utf-8",
        ".mjs": "text/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".webmanifest": "application/manifest+json",
        ".svg": "image/svg+xml",
        ".wasm": "application/wasm",
        ".gz": "application/gzip",
    }

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'wasm-unsafe-eval'; worker-src 'self' blob:; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
        super().end_headers()

server_type = http.server.ThreadingHTTPServer
server_type.daemon_threads = True
handler = functools.partial(Handler, directory=str(root))
try:
    server = server_type(("127.0.0.1", port), handler)
except OSError as error:
    raise SystemExit(f"Could not open port {port}: {error}")

url = f"http://127.0.0.1:{port}/"
print(f"plusultra: {url}")
print("Press Ctrl+C to stop the server.")
if open_browser:
    webbrowser.open(url)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
finally:
    server.server_close()
PY
