# 9. Common Async Bugs and Failure Modes

Async programming is powerful, but it comes with its own set of challenges. Let’s explore some common bugs and how to avoid them.

---

## 1. Forgetting `await`

### The Problem
If you forget to use `await` when calling an async function, the function won’t run as expected. Instead, it will return a coroutine object.

### Example:
```python
import asyncio

async def say_hello():
    print("Hello!")

async def main():
    say_hello()  # Missing `await`

asyncio.run(main())
```

### Output:
Nothing happens! The `say_hello()` function returns a coroutine object, but it’s never executed.

### Solution:
Always use `await` when calling an async function:
```python
await say_hello()
```

---

## 2. Blocking the Event Loop

### The Problem
If you run a blocking operation (e.g., `time.sleep()`), it will freeze the event loop, preventing other tasks from running.

### Example:
```python
import asyncio
import time

async def main():
    time.sleep(2)  # Blocking the event loop
    print("This will be delayed!")

asyncio.run(main())
```

### Solution:
Use `await asyncio.sleep()` instead of `time.sleep()`:
```python
await asyncio.sleep(2)
```

---

## 3. Not Handling Exceptions in Tasks

### The Problem
If an exception occurs in a task created with `asyncio.create_task()`, it won’t be caught unless you explicitly handle it.

### Example:
```python
import asyncio

async def faulty_task():
    raise ValueError("Something went wrong!")

async def main():
    task = asyncio.create_task(faulty_task())
    await task

asyncio.run(main())
```

### Output:
The program crashes with an unhandled exception.

### Solution:
Wrap the task in a `try`-`except` block:
```python
async def main():
    task = asyncio.create_task(faulty_task())
    try:
        await task
    except Exception as e:
        print(f"Caught an exception: {e}")
```

---

## 4. Deadlocks

### The Problem
A deadlock occurs when two tasks are waiting for each other to finish, and neither can proceed.

### Example:
```python
import asyncio

async def task1(lock):
    async with lock:
        await asyncio.sleep(1)
        await task2(lock)  # Waiting for task2

async def task2(lock):
    async with lock:
        await asyncio.sleep(1)
        await task1(lock)  # Waiting for task1

async def main():
    lock = asyncio.Lock()
    await asyncio.gather(task1(lock), task2(lock))

asyncio.run(main())
```

### Solution:
Avoid circular dependencies between tasks. Carefully design your program to prevent tasks from waiting on each other indefinitely.

---

## 5. Overloading the Event Loop

### The Problem
If you schedule too many tasks at once, the event loop can become overloaded, leading to performance issues.

### Example:
```python
import asyncio

async def quick_task():
    await asyncio.sleep(0.1)

async def main():
    tasks = [asyncio.create_task(quick_task()) for _ in range(100000)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

### Solution:
Limit the number of concurrent tasks using a semaphore:
```python
async def limited_task(sem):
    async with sem:
        await asyncio.sleep(0.1)

async def main():
    sem = asyncio.Semaphore(100)  # Limit to 100 concurrent tasks
    tasks = [asyncio.create_task(limited_task(sem)) for _ in range(100000)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

---

## Summary
- Common async bugs include forgetting `await`, blocking the event loop, and not handling exceptions in tasks.
- Deadlocks and event loop overloads can occur if tasks are not managed carefully.
- Use tools like `asyncio.sleep()`, `try`-`except`, and semaphores to avoid these issues.

### Mental Model Takeaway
Think of the event loop as a delicate system that requires careful management to keep tasks running smoothly.

### Intuition You Should Now Have
You should now understand the common pitfalls in async programming and how to avoid them.