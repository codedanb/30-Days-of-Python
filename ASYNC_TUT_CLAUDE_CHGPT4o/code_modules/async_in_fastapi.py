"""
Module: Async in FastAPI

This module demonstrates how to use async programming in FastAPI.
"""
from fastapi import FastAPI
import asyncio
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/slow-task")
async def slow_task():
    """Simulate a slow task."""
    await asyncio.sleep(5)  # Simulate a 5-second delay
    return {"message": "Task complete!"}

@app.get("/stream")
async def stream():
    """Stream data in chunks."""
    async def file_streamer():
        for i in range(10):
            yield f"Chunk {i}\n"
            await asyncio.sleep(1)  # Simulate delay

    return StreamingResponse(file_streamer(), media_type="text/plain")

# Testable function
def test_fastapi():
    print("Run the FastAPI app using: uvicorn async_in_fastapi:app --reload")

if __name__ == "__main__":
    test_fastapi()