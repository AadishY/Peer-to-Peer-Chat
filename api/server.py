from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import asyncio

app = FastAPI()

# In-memory message storage
messages = []

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head><title>Chat Server</title></head>
    <body>
        <h1>Chat Server Running</h1>
        <p>Send and receive messages via the API endpoints.</p>
    </body>
    </html>
    """

@app.get("/messages")
async def get_messages():
    """Endpoint to fetch all messages."""
    return {"messages": messages}

@app.post("/send")
async def send_message(message: str):
    """Endpoint to send a message."""
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    messages.append(message)
    return {"status": "Message sent successfully!"}
