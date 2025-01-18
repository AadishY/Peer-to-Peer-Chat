from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
