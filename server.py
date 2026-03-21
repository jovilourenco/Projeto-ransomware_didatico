import argparse
import base64
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


BASE_DIR = Path(__file__).resolve().parent
PRIVATE_KEY_PATH = BASE_DIR / "private_key.pem"


def load_private_key():
    return serialization.load_pem_private_key(PRIVATE_KEY_PATH.read_bytes(), password=None)


class KeyExchangeHandler(BaseHTTPRequestHandler):
    server_version = "AESRSAExample/1.0"

    def do_GET(self) -> None:
        if self.path != "/health":
            self.send_error(404, "Not found")
            return

        response = {"status": "ok", "message": "Server is healthy."}
        response_bytes = json.dumps(response).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_POST(self) -> None:
        if self.path != "/exchange-key":
            self.send_error(404, "Not found")
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(content_length)
            payload = json.loads(raw_body)
            encrypted_key_b64 = payload["encrypted_key"]
            encrypted_key = base64.b64decode(encrypted_key_b64)
            client_ip = self.client_address[0]

            aes_key = self.server.private_key.decrypt(
                encrypted_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )

            aes_key_b64 = base64.b64encode(aes_key).decode("utf-8")

            print("Client IP:", client_ip)
            print("Encrypted AES key before decrypt (base64):", encrypted_key_b64)
            print("Decrypted AES key after decrypt (base64):", aes_key_b64)

            response = {
                "status": "ok",
                "message": "AES key decrypted successfully on the server.",
            }
            response_bytes = json.dumps(response).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response_bytes)))
            self.end_headers()
            self.wfile.write(response_bytes)
        except Exception as exc:
            response = {"status": "error", "message": str(exc)}
            response_bytes = json.dumps(response).encode("utf-8")
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response_bytes)))
            self.end_headers()
            self.wfile.write(response_bytes)

    def log_message(self, format: str, *args) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser(description="Receive and decrypt an RSA-wrapped AES key.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if not PRIVATE_KEY_PATH.exists():
        raise FileNotFoundError(
            f"Missing {PRIVATE_KEY_PATH}. Run 'python3 generate_keys.py' first."
        )

    httpd = HTTPServer((args.host, args.port), KeyExchangeHandler)
    httpd.private_key = load_private_key()

    print(f"Server listening on http://{args.host}:{args.port}")
    print("GET /health for a health check")
    print("POST the RSA-encrypted AES key to /exchange-key")
    httpd.serve_forever()


if __name__ == "__main__":
    main()

