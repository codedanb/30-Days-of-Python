"""
Module: Streaming, Cancellation, and Long-Lived Async Tasks

This module demonstrates streaming data, handling cancellations, and managing long-lived tasks.
"""
import asyncio
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/stream")
async def stream():
    """Stream data in chunks."""
    async def file_streamer():
        for i in range(5):
            yield f"Chunk {i}\n"
            await asyncio.sleep(1)

    return StreamingResponse(file_streamer(), media_type="text/plain")

async def cancellable_task():
    """Demonstrate a cancellable task."""
    try:
        while True:
            print("Working...")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Task was cancelled!")

async def long_lived_task():
    """Simulate a long-lived task."""
    while True:
        print("Long-lived task running...")
        await asyncio.sleep(5)

# Testable functions
def test_cancellable_task():
    print("--- Cancellable Task ---")
    task = asyncio.create_task(cancellable_task())
    asyncio.run(asyncio.sleep(3))  # Let it run for 3 seconds
    task.cancel()

def test_long_lived_task():
    print("--- Long-Lived Task ---")
    asyncio.run(long_lived_task())

if __name__ == "__main__":
    test_cancellable_task()