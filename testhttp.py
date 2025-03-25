import http.server
import socketserver
import json

PORT = 8545


class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # Send response body
        response = {
            "status": "success",
            "message": "Server is running!",
            "path": self.path,
        }

        self.wfile.write(json.dumps(response).encode("utf-8"))
        return


def run_server():
    # Create server with our handler
    with socketserver.TCPServer(("0.0.0.0", PORT), SimpleHTTPRequestHandler) as httpd:
        print(f"Server started at 0.0.0.0:{PORT}")
        # Serve until interrupted
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped.")


# if __name__ == "__main__":
#     run_server()
