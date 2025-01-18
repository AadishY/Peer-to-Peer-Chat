from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

# In-memory message queue (could use database in real app)
messages = []

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
        // Fetch the chat messages every second (long polling)
        setInterval(() => {
            fetch("/polling")
                .then(response => response.json())
                .then(data => {
                    const logs = document.getElementById("logs");
                    data.messages.forEach(msg => {
                        const message = document.createElement('div');
                        message.textContent = msg;
                        logs.appendChild(message);
                    });
                })
                .catch(error => {
                    console.error("Error fetching messages:", error);
                });
        }, 1000);  // Polling every 1 second
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def serve_html():
    # Return the HTML content as the homepage
    return html_content

@app.get("/polling")
def polling():
    # Return the latest chat messages (simulating long polling)
    return {"messages": messages}

@app.post("/send_message")
def send_message(message: str):
    # Store the new message
    messages.append(message)
    return {"status": "Message received"}
