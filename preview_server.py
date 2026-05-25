from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os
import socket
import sys
import traceback
import webbrowser


ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 4173
LOG_FILE = ROOT / "preview_server.log"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return


def find_free_port(start_port, attempts=20):
    for port in range(start_port, start_port + attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            try:
                probe.bind((HOST, port))
            except OSError:
                continue
            return port
    raise OSError(f"No free preview port found from {start_port} to {start_port + attempts - 1}.")


def main():
    os.chdir(ROOT)
    port = find_free_port(PORT)
    url = f"http://{HOST}:{port}/"
    print("=" * 56)
    print("Prophet TV Hub preview is running.")
    print(f"Open this URL in your browser: {url}")
    print("Keep this window open while previewing. Press Ctrl+C to stop.")
    print("=" * 56)

    if os.environ.get("PTV_PREVIEW_NO_BROWSER") != "1":
        webbrowser.open(url)

    with ThreadingHTTPServer((HOST, port), QuietHandler) as server:
        server.serve_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPreview server stopped.")
    except Exception:
        error = traceback.format_exc()
        LOG_FILE.write_text(error, encoding="utf-8")
        print("Preview server failed to start.")
        print(error)
        if sys.stdin and sys.stdin.isatty():
            input("Press Enter to close this window...")
