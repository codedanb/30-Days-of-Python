# 11. Compare Async vs Threads

Async programming and threads are two different ways to achieve concurrency. Let’s compare them to understand their strengths, weaknesses, and when to use each.

---

## What Are Threads?

A thread is a lightweight unit of execution within a process. Threads allow a program to perform multiple tasks at the same time by running them in parallel.

### Example:
Imagine a bakery with multiple bakers:
- Each baker (thread) works on a different task (e.g., baking bread, making cakes).
- They work independently but share the same kitchen (process).

---

## Key Differences

| Feature               | Async Programming                  | Threads                          |
|-----------------------|-------------------------------------|----------------------------------|
| **Concurrency Model** | Cooperative multitasking           | Preemptive multitasking          |
| **Execution**         | Single-threaded                    | Multi-threaded                   |
| **Blocking**          | Non-blocking                       | Can block                        |
| **Performance**       | Efficient for I/O-bound tasks      | Better for CPU-bound tasks       |
| **Complexity**        | Requires async/await syntax        | Requires thread management       |
| **Overhead**          | Low (no context switching)         | Higher (context switching costs) |

---

## When to Use Async

Async is ideal for:
- **I/O-Bound Tasks:** Tasks that spend a lot of time waiting, such as:
  - Fetching data from a database.
  - Downloading files.
  - Calling APIs.
- **High Concurrency:** Handling thousands of connections efficiently (e.g., web servers).

### Example: Async Web Server
An async web server can handle multiple requests concurrently without creating a new thread for each request.

---

## When to Use Threads

Threads are better for:
- **CPU-Bound Tasks:** Tasks that require heavy computation, such as:
  - Image processing.
  - Data analysis.
  - Machine learning.
- **Parallel Execution:** Utilizing multiple CPU cores.

### Example: Threaded Image Processing
A threaded program can process multiple images in parallel, using all available CPU cores.

---

## Combining Async and Threads

In some cases, you can combine async and threads to get the best of both worlds. For example:
- Use async for I/O-bound tasks.
- Use threads for CPU-bound tasks.

### Example:
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def cpu_bound_task():
    # Simulate a CPU-intensive task
    result = sum(i * i for i in range(10**6))
    return result

async def main():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_bound_task)
        print(f"Result: {result}")

asyncio.run(main())
```

### Explanation:
- `ThreadPoolExecutor`: Runs CPU-bound tasks in a separate thread.
- `loop.run_in_executor()`: Allows async code to offload work to threads.

---

## Summary
- **Async** is best for I/O-bound tasks and high concurrency.
- **Threads** are better for CPU-bound tasks and parallel execution.
- You can combine async and threads to handle both I/O-bound and CPU-bound tasks efficiently.

### Mental Model Takeaway
Think of async as a single multitasking worker and threads as multiple workers running in parallel.

### Intuition You Should Now Have
You should now understand the strengths and weaknesses of async and threads, and when to use each.