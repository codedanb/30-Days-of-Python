# 12. Streaming, Cancellation, and Long-Lived Async Tasks

Async programming is not just about handling short tasks. It’s also great for managing long-lived tasks, streaming data, and handling cancellations gracefully.

---

## Streaming Data

Streaming is the process of sending data in chunks instead of all at once. Async makes streaming efficient because it can handle each chunk as it arrives without blocking.

### Example: Streaming a File
Here’s how to stream a file in FastAPI:

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def file_streamer():
    for i in range(10):
        yield f"Chunk {i}\n"
        await asyncio.sleep(1)  # Simulate delay

@app.get("/stream")
async def stream():
    return StreamingResponse(file_streamer(), media_type="text/plain")
```

### Explanation:
- `yield`: Sends a chunk of data to the client.
- `await asyncio.sleep(1)`: Simulates a delay between chunks.
- `StreamingResponse`: Sends the data to the client as it’s generated.

---

## Handling Cancellations

Sometimes, you need to cancel a task before it completes. Async makes this possible with `asyncio.CancelledError`.

### Example: Cancelling a Task
```python
import asyncio

async def long_task():
    try:
        while True:
            print("Working...")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Task was cancelled!")

async def main():
    task = asyncio.create_task(long_task())
    await asyncio.sleep(3)  # Let the task run for 3 seconds
    task.cancel()  # Cancel the task
    await task  # Wait for the task to handle the cancellation

asyncio.run(main())
```

### Explanation:
- `task.cancel()`: Sends a cancellation signal to the task.
- `asyncio.CancelledError`: Raised inside the task when it’s cancelled.

---

## Long-Lived Tasks

Long-lived tasks are tasks that run for an extended period, such as:
- Monitoring a server.
- Listening for messages.
- Running background jobs.

### Example: Background Task in FastAPI

FastAPI supports background tasks using `BackgroundTasks`:

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def background_job(name: str):
    with open("log.txt", "a") as f:
        f.write(f"Hello, {name}!\n")

@app.get("/start-job")
async def start_job(background_tasks: BackgroundTasks, name: str):
    background_tasks.add_task(background_job, name)
    return {"message": "Job started!"}
```

### Explanation:
- `BackgroundTasks`: Runs the task in the background without blocking the main thread.
- `add_task()`: Schedules the background job.

---

## Summary
- **Streaming**: Use `yield` and `StreamingResponse` to send data in chunks.
- **Cancellations**: Use `task.cancel()` and handle `asyncio.CancelledError` to stop tasks gracefully.
- **Long-Lived Tasks**: Use background tasks for jobs that run for an extended period.

### Mental Model Takeaway
Think of streaming as sending data piece by piece, cancellations as politely stopping a task, and long-lived tasks as background workers.

### Intuition You Should Now Have
You should now understand how to handle streaming, cancellations, and long-lived tasks in async programming.