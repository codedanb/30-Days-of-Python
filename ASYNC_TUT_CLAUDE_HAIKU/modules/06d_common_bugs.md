# Module 6d: Common Async Bugs and Failure Modes

## The Dark Side: Where Things Go Wrong

Now that you understand async, let's talk about what breaks. These are real bugs that catch even experienced developers.

## Bug 1: Forgetting `await`

The most common async bug:

```python
async def main():
    result = fetch_data()  # Forgot await!
    print(result)
    
asyncio.run(main())
```

Output:
```
<coroutine object fetch_data at 0x7f8...>
```

**What happened:**
- `fetch_data()` returns a coroutine object, not the data
- The coroutine never runs
- You print the coroutine object itself

**The fix:**
```python
result = await fetch_data()  # Added await
```

**Why it's sneaky:**
- No error is raised (it's valid Python)
- The code runs without crashing
- But it doesn't do what you expect

**How to catch it:**
- Your type checker (mypy, pyright) should warn you
- Look for `<coroutine object>` in output
- Use a linter that checks for unawaited coroutines

## Bug 2: Creating a Task But Not Awaiting It

```python
async def main():
    task = asyncio.create_task(slow_function())  # Task created
    # Do something else
    # Maybe return from the function
    # Task is lost!

asyncio.run(main())
```

What happens:
- Task is created and scheduled
- But you lose the reference to it
- It runs in the background
- When main() returns, the event loop might exit before the task finishes
- You never see the result

**The problem case:**

```python
async def main():
    # Create multiple tasks
    for i in range(5):
        asyncio.create_task(download_file(i))  # Created but not stored
    
    print("All downloads started")
    # main returns
    # The tasks haven't finished yet!

asyncio.run(main())
print("Done")
```

Output:
```
All downloads started
Done
```

Wait, where are the downloaded files? The event loop exited before they finished.

**The fix:**

```python
async def main():
    tasks = [asyncio.create_task(download_file(i)) for i in range(5)]
    await asyncio.gather(*tasks)
    print("All downloads done")

asyncio.run(main())
```

**Best practice:** If you create a task, always await it (directly or via gather).

## Bug 3: Race Conditions

When multiple tasks access shared data unsafely:

```python
counter = 0

async def increment():
    global counter
    for _ in range(1000000):
        counter += 1  # This is not atomic!

async def main():
    await asyncio.gather(
        increment(),
        increment(),
        increment(),
    )
    print(f"Counter: {counter}")
    # Expected: 3000000
    # Actual: Some number less than 3000000

asyncio.run(main())
```

**What's happening:**

The line `counter += 1` is actually three operations:
1. Read counter
2. Add 1
3. Write back

All three tasks are doing this concurrently:

```
Task A: Read counter (value: 5)
Task B: Read counter (value: 5)
Task A: Add 1 (now 6)
Task B: Add 1 (now 6)
Task A: Write back (counter is now 6)
Task B: Write back (counter is now 6)  # Lost one increment!
```

The final value is 6 instead of 7.

**The fix:**

Use asyncio primitives for synchronization:

```python
counter = 0
lock = asyncio.Lock()

async def increment():
    global counter
    for _ in range(1000000):
        async with lock:  # Hold the lock
            counter += 1  # Now atomic

async def main():
    await asyncio.gather(
        increment(),
        increment(),
        increment(),
    )
    print(f"Counter: {counter}")
    # Now: 3000000 (correct)

asyncio.run(main())
```

**When you need to share data between async tasks, use:**
- `asyncio.Lock()`
- `asyncio.Event()`
- `asyncio.Queue()`
- Other synchronization primitives

## Bug 4: Blocking the Event Loop

If you do something CPU-intensive in an async function, you block the entire event loop:

```python
import time

async def cpu_intensive():
    # This blocks the event loop for 5 seconds
    time.sleep(5)  # NEVER DO THIS IN ASYNC CODE
    return "done"

async def other_task():
    print("Starting other task")
    for i in range(5):
        print(f"Step {i}")
        await asyncio.sleep(0.1)
    print("Other task done")

async def main():
    await asyncio.gather(
        cpu_intensive(),
        other_task(),
    )

asyncio.run(main())
```

Output:
```
Starting other task
[5 second freeze while cpu_intensive runs]
Other task done
Step 0
Step 1
Step 2
Step 3
Step 4
```

Notice: `other_task()` waits for `cpu_intensive()` to finish before it can even start its first step.

**Why:** `time.sleep()` blocks the entire thread. The event loop can't run anything else.

**The fix:**

Use `asyncio.sleep()` instead:

```python
async def cpu_intensive():
    # This doesn't block the event loop
    await asyncio.sleep(5)
    return "done"
```

But wait, `asyncio.sleep()` doesn't do CPU work. It just sleeps.

For actual CPU-intensive work, you need:

```python
async def main():
    # Run CPU-intensive work in a thread pool
    result = await asyncio.get_event_loop().run_in_executor(
        None,  # Use default executor
        intensive_calculation
    )
    print(result)
```

## Bug 5: Deadlocks

If tasks wait for each other, you can get deadlocks:

```python
async def task_a():
    print("A: waiting for B")
    await task_b()  # Wait for B to complete
    print("A: B is done")

async def task_b():
    print("B: waiting for A")
    await task_a()  # Wait for A to complete
    print("B: A is done")

async def main():
    await asyncio.gather(
        task_a(),
        task_b(),
    )

asyncio.run(main())
```

**What happens:**
- A waits for B
- B waits for A
- Neither can progress
- Deadlock
- Program hangs forever (until timeout)

**How to avoid:**
- Don't have circular dependencies
- Use proper coordination (queues, events)
- Structure code so dependencies are clear

## Bug 6: Uncaught Exceptions in Background Tasks

If an exception happens in a task you're not awaiting:

```python
async def background_error():
    await asyncio.sleep(0.1)
    raise ValueError("Something went wrong!")

async def main():
    task = asyncio.create_task(background_error())
    
    print("Task started")
    # We don't await it
    # When the exception happens, we won't see it
    
    await asyncio.sleep(1)

asyncio.run(main())
```

The exception might be silently lost. You'll only see it when:
- The task is garbage collected
- You explicitly check the task's exception

**Better:**

```python
async def main():
    task = asyncio.create_task(background_error())
    
    try:
        await task
    except ValueError as e:
        print(f"Caught: {e}")
```

Or use task callbacks:

```python
def handle_exception(task):
    try:
        task.result()
    except Exception as e:
        print(f"Task failed: {e}")

async def main():
    task = asyncio.create_task(background_error())
    task.add_done_callback(handle_exception)
    
    await asyncio.sleep(1)
```

## Bug 7: Event Loop Not Running

```python
async def main():
    await asyncio.sleep(1)
    return "done"

# This doesn't work
result = main()
print(result)  # <coroutine object>
```

The coroutine is created but never runs. You must use `asyncio.run()`:

```python
result = asyncio.run(main())
print(result)  # "done"
```

## Bug 8: Mixing Sync and Async Badly

```python
# DON'T DO THIS
def sync_function():
    result = asyncio.run(async_function())
    return result

async def main():
    result = sync_function()  # Can't call sync that runs its own event loop
```

If `sync_function()` is called from an async context, `asyncio.run()` fails because there's already an event loop.

**Solution:** Keep sync and async separate, or use `run_in_executor()`.

---

## Common Anti-Patterns and Solutions

### Anti-Pattern 1: Sequential When You Mean Concurrent

```python
# ✗ Wrong (sequential)
async def main():
    result1 = await fetch(1)
    result2 = await fetch(2)
    result3 = await fetch(3)

# ✓ Right (concurrent)
async def main():
    results = await asyncio.gather(
        fetch(1),
        fetch(2),
        fetch(3),
    )
```

### Anti-Pattern 2: Not Handling Timeouts

```python
# ✗ Wrong (might hang forever)
result = await external_api_call()

# ✓ Right (protected)
try:
    result = await asyncio.wait_for(external_api_call(), timeout=5)
except asyncio.TimeoutError:
    # Handle timeout
    pass
```

### Anti-Pattern 3: Creating Too Many Tasks

```python
# ✗ Wrong (creates millions of tasks, runs out of memory)
tasks = [
    asyncio.create_task(process_item(item))
    for item in huge_list  # 1 million items
]
await asyncio.gather(*tasks)

# ✓ Right (semaphore limits concurrency)
semaphore = asyncio.Semaphore(100)  # Max 100 concurrent

async def limited_process(item):
    async with semaphore:
        return await process_item(item)

tasks = [
    asyncio.create_task(limited_process(item))
    for item in huge_list
]
await asyncio.gather(*tasks)
```

---

## Debugging Async Code

### Technique 1: Print Statements

```python
import time

async def task(name):
    print(f"[{time.time():.2f}] {name} starting")
    await asyncio.sleep(1)
    print(f"[{time.time():.2f}] {name} done")

async def main():
    await asyncio.gather(
        task("A"),
        task("B"),
    )

asyncio.run(main())
```

Output shows the timeline clearly.

### Technique 2: Task Names

```python
async def main():
    task = asyncio.create_task(slow_function(), name="my_task")
    print(task.get_name())
```

### Technique 3: Debug Mode

```python
import logging

logging.basicConfig(level=logging.DEBUG)

asyncio.run(main(), debug=True)
```

This logs all events.

### Technique 4: Exception Groups (Python 3.11+)

```python
async def main():
    try:
        await asyncio.gather(
            failing_task1(),
            failing_task2(),
        )
    except ExceptionGroup as eg:
        for exc in eg.exceptions:
            print(f"Task failed: {exc}")
```

---

## Summary

- **Forgetting `await`**: Most common bug, use type checking
- **Lost tasks**: Always await tasks you create
- **Race conditions**: Use async synchronization primitives
- **Blocking the loop**: Use `await asyncio.sleep()`, not `time.sleep()`
- **Deadlocks**: Avoid circular dependencies
- **Uncaught exceptions**: Explicitly handle task exceptions
- **Event loop issues**: Use `asyncio.run()` and keep sync/async separate

## Mental Model Takeaway

Async bugs are usually about **control flow surprises**:
- Code doesn't run when you think it will
- Code runs after you think it's done
- Multiple copies of code run at the same time accessing the same data
- The event loop is blocked

Most bugs come from forgetting that **async doesn't change the single-threaded execution model**, it just schedules it differently.

## What You Should Now Understand

- The most common async bugs and how they happen
- How to debug async code
- Common anti-patterns and their fixes
- Synchronization primitives (Lock, Event, Queue)
- How to handle exceptions in background tasks
- How to limit concurrency when needed
- That async simplifies concurrency but introduces new categories of bugs

---

Next: applying async to the real world with FastAPI, building web servers, and seeing async at scale.
