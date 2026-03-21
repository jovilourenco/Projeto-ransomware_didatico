import json
import socket
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


BASE_DIR = Path(__file__).resolve().parent
ENCRYPTED_KEY_PATH = BASE_DIR / "key.bin.enc"


class HealthCheckError(RuntimeError):
    pass


class KeyExchangeError(RuntimeError):
    pass


def build_healthcheck_url(server_url: str) -> str:
    parsed_url = urlsplit(server_url)
    return urlunsplit(
        (parsed_url.scheme, parsed_url.netloc, "/health", "", "")
    )


def check_server_health(server_url: str, timeout: float = 2.0) -> dict:
    healthcheck_url = build_healthcheck_url(server_url)
    request = urllib.request.Request(healthcheck_url, method="GET")

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response_body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise HealthCheckError(
            f"Health check failed: server returned HTTP {exc.code} for {healthcheck_url}."
        ) from exc
    except urllib.error.URLError as exc:
        reason = exc.reason
        if isinstance(reason, TimeoutError) or isinstance(reason, socket.timeout):
            raise HealthCheckError(
                f"Health check timed out after {timeout:.1f}s for {healthcheck_url}."
            ) from exc
        if isinstance(reason, ConnectionRefusedError):
            raise HealthCheckError(
                f"Health check failed: connection refused for {healthcheck_url}. Is the server running?"
            ) from exc
        raise HealthCheckError(
            f"Health check failed: could not reach {healthcheck_url} ({reason})."
        ) from exc

    try:
        health_data = json.loads(response_body)
    except json.JSONDecodeError as exc:
        raise HealthCheckError(
            f"Health check failed: {healthcheck_url} did not return valid JSON."
        ) from exc

    if health_data.get("status") != "ok":
        raise HealthCheckError(
            f"Health check failed: unexpected response from {healthcheck_url}: {health_data}"
        )

    return health_data


def load_encrypted_key(key_path: Path = ENCRYPTED_KEY_PATH) -> str:
    if not key_path.exists():
        raise FileNotFoundError(
            f"Missing {key_path}. Put the RSA-encrypted AES key there first."
        )

    encrypted_key_b64 = key_path.read_text(encoding="utf-8").strip()
    if not encrypted_key_b64:
        raise ValueError(f"{key_path} is empty. Put the RSA-encrypted AES key there first.")

    return encrypted_key_b64


def send_encrypted_aes_key(
    encrypted_key_b64: str,
    server_url: str = "http://127.0.0.1:8000/exchange-key",
) -> dict:
    check_server_health(server_url)

    payload = json.dumps(
        {"encrypted_key": encrypted_key_b64}
    ).encode("utf-8")

    request = urllib.request.Request(
        server_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        response_body = exc.read().decode("utf-8", errors="replace")
        try:
            error_data = json.loads(response_body)
            error_message = error_data.get("message", response_body)
        except json.JSONDecodeError:
            error_message = response_body or exc.reason
        raise KeyExchangeError(
            f"Key exchange failed: server returned HTTP {exc.code}: {error_message}"
        ) from exc
    except urllib.error.URLError as exc:
        raise KeyExchangeError(
            f"Key exchange failed: could not reach {server_url} ({exc.reason})."
        ) from exc
