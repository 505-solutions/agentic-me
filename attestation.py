import json
import socket
from http.client import HTTPConnection
from pathlib import Path


def get_simulated_token() -> str:
    """Reads the first line from a given file path."""
    with (Path(__file__).parent / "simulated_token.txt").open("r") as f:
        return f.readline().strip()


SIM_TOKEN = get_simulated_token()


def check_nonce_length(nonces: list[str]) -> None:
    min_byte_len = 10
    max_byte_len = 74
    for nonce in nonces:
        byte_len = len(nonce.encode("utf-8"))
        if byte_len < min_byte_len or byte_len > max_byte_len:
            msg = f"Nonce '{nonce}' must be between {min_byte_len} bytes"
            f" and {max_byte_len} bytes"
            raise RuntimeError(msg)


def get_token(
    nonces: list[str],
    simulate: bool = False,
    audience: str = "https://sts.google.com",
    token_type: str = "OIDC",  # noqa: S107
) -> str:

    check_nonce_length(nonces)
    if simulate:
        return SIM_TOKEN

    url: str = "http://localhost/v1/token"
    unix_socket_path: str = "/run/container_launcher/teeserver.sock"

    # Connect to the socket
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client_socket.connect(unix_socket_path)

    # Create an HTTP connection object
    conn = HTTPConnection("localhost", timeout=10)
    conn.sock = client_socket

    # Send a POST request
    headers = {"Content-Type": "application/json"}
    body = json.dumps(
        {"audience": audience, "token_type": token_type, "nonces": nonces}
    )
    conn.request("POST", url, body=body, headers=headers)

    # Get and decode the response
    res = conn.getresponse()
    success_status = 200
    if res.status != success_status:
        msg = f"Failed to get attestation response: {res.status} {res.reason}"
        raise RuntimeError(msg)
    token = res.read().decode()

    # Close the connection
    conn.close()
    return token
