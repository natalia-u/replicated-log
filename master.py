from fastapi import FastAPI
import httpx
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("master")

app = FastAPI()

messages = []
SECONDARY_URLS = [
    "http://secondary1-container:8001",
    "http://secondary2-container:8001"
]

@app.get("/messages")
def get_messages():
    return messages

async def replicate_to_secondary(client, secondary_url, message):
    response = await client.post(
        f"{secondary_url}/replicate",
        params={"message": message}
    )
    return response

@app.post("/messages")
async def add_message(message: str):
    messages.append(message)
    logger.info(f"Message added to Master: {message}")

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [
            replicate_to_secondary(client, secondary_url, message)
            for secondary_url in SECONDARY_URLS
        ]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            if response.status_code != 200:
                return {"status": "replication failed"}

        logger.info(f"Message replicated to all Secondaries: {message}")
        return {"status": "ok"}