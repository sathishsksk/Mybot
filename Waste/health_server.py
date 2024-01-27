import asyncio
import http.server
import os

HEALTH_PORT = int(os.getenv("HEALTH_PORT", 8081))

class HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

async def health_server():
    async def run_health_server():
        server_address = ("", HEALTH_PORT)
        httpd = http.server.HTTPServer(server_address, HealthHandler)
        httpd.serve_forever()

    asyncio.create_task(run_health_server())

if __name__ == "__main__":
    asyncio.run(health_server())
