# Async Programming Quick Reference Guide

A quick lookup guide for common async patterns and concepts.

## Quick Start

```python
import asyncio

# Define an async function
async def hello():
    await asyncio.sleep(1)
    return "done"

# Run it
result = asyncio.run(hello())
```

## Essential Keywords

### `async def`
Defines an async function. Can use `await` inside it.

```python
async def my_function():
    pass
```

### `await`
Pauses the function and gives control to the event loop.

```python
result = await some_async_function()
```

**Remember:** Only use `await` inside `async def` functions.

### `asyncio.run()`
Creates an event loop, runs an async function, and cleans up.

```python
asyncio.run(my_async_function())
```

Use this at the top level (not inside other async functions).

---

## Common Patterns

### Pattern: Run Multiple Tasks Concurrently

```python
async def main():
    # Create tasks
    task1 = asyncio.create_task(fetch(1))
    task2 = asyncio.create_task(fetch(2))
    
    # Wait for all
    results = await asyncio.gather(task1, task2)
    
asyncio.run(main())
```

### Pattern: Sequential (Await One After Another)

```python
async def main():
    # These run one after another
    result1 = await fetch(1)
    result2 = await fetch(2)
    
asyncio.run(main())
```

**Key difference:**
- Sequential: task 2 waits for task 1 to finish
- Concurrent: both run at the same time

### Pattern: Wait for First

```python
async def main():
    task1 = asyncio.create_task(fetch(1))
    task2 = asyncio.create_task(fetch(2))
    
    done, pending = await asyncio.wait(
        [task1, task2],
        return_when=asyncio.FIRST_COMPLETED
    )
    
    # Get the result
    result = done.pop().result()
    
    # Cancel the rest
    for task in pending:
        task.cancel()
```

### Pattern: Timeout

```python
try:
    result = await asyncio.wait_for(
        fetch_data(),
        timeout=5.0
    )
except asyncio.TimeoutError:
    print("Timed out!")
```

### Pattern: Rate Limiting

```python
semaphore = asyncio.Semaphore(3)  # Max 3 concurrent

async def limited_fetch(item_id):
    async with semaphore:
        return await fetch(item_id)
```

### Pattern: Loop with Delay

```python
while True:
    await asyncio.sleep(5)  # Do something every 5 seconds
    await do_something()
```

### Pattern: Cancellation

```python
task = asyncio.create_task(long_running())

await asyncio.sleep(1)
task.cancel()

try:
    await task
except asyncio.CancelledError:
    print("Cancelled")
```

---

## Common Mistakes and Fixes

### Mistake 1: Forgetting `await`

```python
# ✗ Wrong
result = fetch_data()  # Returns coroutine, not data

# ✓ Right
result = await fetch_data()
```

### Mistake 2: Creating Task But Not Awaiting

```python
# ✗ Wrong
asyncio.create_task(background_work())  # Task is lost

# ✓ Right
task = asyncio.create_task(background_work())
await task
```

### Mistake 3: Using `time.sleep()` Instead of `asyncio.sleep()`

```python
# ✗ Wrong - blocks event loop
time.sleep(1)

# ✓ Right - doesn't block
await asyncio.sleep(1)
```

### Mistake 4: Not Using `async def`

```python
# ✗ Wrong
def fetch():
    await external_api()  # Error!

# ✓ Right
async def fetch():
    await external_api()
```

### Mistake 5: Forgetting `asyncio.run()`

```python
# ✗ Wrong
result = main()  # Returns coroutine, doesn't run

# ✓ Right
result = asyncio.run(main())
```

---

## Decision Tree: Which Pattern to Use

```
Do you want...

→ Run multiple tasks, wait for all?
  Use: asyncio.gather()
  
→ Run multiple tasks, use first result?
  Use: asyncio.wait(FIRST_COMPLETED)
  
→ Run multiple tasks, process as they arrive?
  Use: asyncio.as_completed()
  
→ Run with timeout?
  Use: asyncio.wait_for()
  
→ Limit concurrent operations?
  Use: asyncio.Semaphore()
  
→ Retry on failure?
  Use: try/except with loop
  
→ Stop a running task?
  Use: task.cancel()
```

---

## Async vs Sync Decision Tree

```
Do you have...

→ Many I/O-bound tasks (network, database, files)?
  Use: ASYNC
  
→ Need to handle 100+ concurrent connections?
  Use: ASYNC
  
→ CPU-intensive work (calculations, processing)?
  Use: MULTIPROCESSING
  
→ Lightweight threading needed?
  Use: THREADING
  
→ Legacy sync libraries that can't be rewritten?
  Use: THREADING or run_in_executor()
  
→ Unsure?
  Default: ASYNC for I/O, MULTIPROCESSING for CPU
```

---

## Debugging Async Code

### Print statement debugging

```python
import time

async def my_function():
    print(f"[{time.time():.2f}] Starting")
    await asyncio.sleep(1)
    print(f"[{time.time():.2f}] Done")
```

### Task names

```python
task = asyncio.create_task(my_function(), name="my_task")
print(task.get_name())
```

### Check task result

```python
task = asyncio.create_task(my_function())
await asyncio.sleep(2)

if task.done():
    print(task.result())
```

### Get all running tasks

```python
tasks = asyncio.all_tasks()
for task in tasks:
    print(task)
```

### Enable debug mode

```python
asyncio.run(main(), debug=True)
```

---

## FastAPI with Async

### Basic endpoint

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello"}
```

### Endpoint with async operation

```python
import asyncio

@app.get("/data")
async def get_data():
    await asyncio.sleep(1)  # Simulate slow operation
    return {"data": "value"}
```

### Endpoint with multiple async operations

```python
async def fetch_user(user_id):
    await asyncio.sleep(0.5)
    return {"id": user_id}

async def fetch_posts(user_id):
    await asyncio.sleep(0.5)
    return {"user_id": user_id, "posts": []}

@app.get("/user/{user_id}/profile")
async def get_profile(user_id: int):
    user, posts = await asyncio.gather(
        fetch_user(user_id),
        fetch_posts(user_id),
    )
    return {"user": user, "posts": posts}
```

---

## Common Async Functions

### Sleep

```python
await asyncio.sleep(1)  # Sleep for 1 second
```

### Gather (run multiple concurrently)

```python
results = await asyncio.gather(task1, task2, task3)
```

### Create task (schedule for later)

```python
task = asyncio.create_task(my_function())
```

### Wait for first

```python
done, pending = await asyncio.wait(
    [task1, task2],
    return_when=asyncio.FIRST_COMPLETED
)
```

### Wait with timeout

```python
await asyncio.wait_for(my_function(), timeout=5.0)
```

### For loop over results as they arrive

```python
for coro in asyncio.as_completed(tasks):
    result = await coro
```

### Queue (producer-consumer)

```python
queue = asyncio.Queue()
await queue.put(item)
item = await queue.get()
```

### Lock (prevent race conditions)

```python
lock = asyncio.Lock()
async with lock:
    # Only one task can be here at a time
    pass
```

### Event (signal between tasks)

```python
event = asyncio.Event()
await event.wait()  # Wait until set
event.set()  # Signal
```

### Semaphore (limit concurrent)

```python
semaphore = asyncio.Semaphore(3)
async with semaphore:
    # Only 3 tasks here at a time
    pass
```

---

## Performance Tips

1. **Use `asyncio.gather()` for concurrency** - don't `await` one after another
2. **Use `asyncio.sleep()` not `time.sleep()`** - async sleep doesn't block
3. **Use connection pooling** - reuse connections to database/API
4. **Use semaphores for rate limiting** - don't create unlimited concurrent tasks
5. **Use queues for producer-consumer** - natural backpressure
6. **Set timeouts** - don't wait forever for slow services
7. **Monitor tasks** - check if background tasks are still running

---

## When to Use What

### Use Async When
- Handling many I/O operations (network, database, files)
- Building web servers (FastAPI, aiohttp)
- Need to handle 100+ concurrent connections
- Want simple-looking code that's actually concurrent
- Available async libraries (httpx, asyncpg, etc.)

### Use Threading When
- Have 10-50 concurrent connections
- Must use sync libraries (no async equivalent)
- Complexity of async isn't worth it
- Already know threading

### Use Multiprocessing When
- CPU-intensive work (calculations, processing)
- Have multiple cores to use
- Need true parallelism
- Can serialize/pickle data

### Use Regular Sync Code When
- Simple scripts
- CPU-bound work that fits in one process
- No concurrency needed
- Keeping it simple

---

## Resources

- [Official asyncio docs](https://docs.python.org/3/library/asyncio.html)
- [FastAPI async docs](https://fastapi.tiangolo.com/async-and-await/)
- [Real Python async tutorials](https://realpython.com/async-io-python/)
- [asyncio source code](https://github.com/python/cpython/blob/main/Lib/asyncio/)

---

## Key Takeaways

1. **Async is for I/O-bound concurrency**, not parallelism
2. **Event loop schedules tasks**, pausing at `await` points
3. **`await` creates pause points** that let the event loop schedule other tasks
4. **No blocking allowed** - use `asyncio.sleep()` not `time.sleep()`
5. **Most common bug is forgetting `await`** - check your code
6. **Use `asyncio.gather()` for concurrency**, not sequential `await`s
7. **Set timeouts** - don't wait forever
8. **Async looks sequential but runs concurrently** - that's the magic

---

Keep this guide bookmarked for quick reference while learning and using async!
