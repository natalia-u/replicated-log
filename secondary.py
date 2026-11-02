from fastapi import FastAPI
import asyncio
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("secondary")

app = FastAPI()

messages = []

@app.get("/messages")
def get_messages():
    return messages

@app.post("/replicate")
async def replicate_message(message: str):
    delay = int(os.getenv("DELAY", "0"))
    await asyncio.sleep(delay)

    messages.append(message)
    logger.info(f"Message replicated to Secondary: {message}")
    
    return {"status": "ok"}