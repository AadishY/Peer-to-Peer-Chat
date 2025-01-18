from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import socket
import asyncio
from typing import List

app = FastAPI()

clients = []

# HTML content for the website
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Server Logs</title>
</head>
<body>
    <h1>Chat Server Logs</h1>
    <h2 id="ws-url">Loading WebSocket URL...</h2>
    <div id="logs"></div>
    <script>
        // Fetch the WebSocket URL from the server
        fetch("/")
            .then(response => response.json())
            .then(data => {
                document.getElementById("ws-url").textContent = `WebSocket URL: ${data["WebSocket URL"]}`;
                connectWebSocket(data["WebSocket URL"]);
            })
            .catch(error => {
                document.getElementById("ws-url").textContent = "Error fetching WebSocket URL.";
                console.error(error);
            });

        function connectWebSocket(url) {
            const logs = document.getElementById("logs");
            const ws = new WebSocket(url);

            ws.onmessage = (event) => {
                const message = document.createElement('div');
                message.textContent = event.data;
                logs.appendChild(message);
            };

            ws.onclose = () => {
                const message = document.createElement('div');
                message.textContent = "Connection closed.";
                logs.appendChild(message);
            };
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def serve_html():
    # Return the HTML content as the homepage
    return html_content

@app.get("/ws-url")
def get_ws_url():
    host = socket.gethostbyname(socket.gethostname())
    ws_url = f"ws://{host}:8000/ws"  # Adjust the port if needed
    return {"WebSocket URL": ws_url}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast the received message to all clients
            for client in clients:
                if client != websocket:
                    await client.send_text(data)
    except WebSocketDisconnect:
        clients.remove(websocket)
