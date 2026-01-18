# Module 6f: Async vs Threads vs Processes — When to Use Each

## The Comparison That Matters

You now know async deeply. But there are other ways to handle concurrency: threads and processes. When should you use each? This is crucial for picking the right tool.

## The Three Approaches to Concurrency

### 1. Async (asyncio)

**How it works:** Single thread, event loop schedules tasks, tasks pause explicitly with `await`

**Code:**
```python
import asyncio

async def task(name):
    await asyncio.sleep(1)
    return f"Result {name}"

async def main():
    results = await asyncio.gather(
        task("A"), task("B"), task("C")
    )
    print(results)

asyncio.run(main())
```

**Execution:**
```
Single thread, multiple tasks scheduled by event loop
0.0s: A, B, C start (await asyncio.sleep)
1.0s: All done
Total: 1 second
```

### 2. Threading

**How it works:** Multiple threads, OS handles scheduling, preemptive interrupts

**Code:**
```python
import threading

def task(name):
    time.sleep(1)
    return f"Result {name}"

threads = []
for name in ["A", "B", "C"]:
    t = threading.Thread(target=task, args=(name,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
```

**Execution:**
```
Three threads, OS schedules them
0.0s: A, B, C start (time.sleep)
1.0s: All done
Total: ~1 second (might vary slightly)
```

### 3. Multiprocessing

**How it works:** Multiple processes, true parallelism, no shared memory

**Code:**
```python
import multiprocessing

def task(name):
    time.sleep(1)
    return f"Result {name}"

with multiprocessing.Pool(3) as pool:
    results = pool.map(task, ["A", "B", "C"])
    print(results)
```

**Execution:**
```
Three processes on three CPU cores (if available)
0.0s: A, B, C start (time.sleep)
1.0s: All done
Total: ~1 second (true parallelism)
```

## Quick Comparison

```
                Async       Threads     Processes
─────────────────────────────────────────────────
Memory          Low         Medium      High
Startup         Fast        Fast        Slow
Context switch  Cooperative Preemptive  OS-scheduled
I/O-bound       ✓✓✓         ✓✓          ✓
CPU-bound       ✗           ✗ (GIL)     ✓✓✓
Shared memory   Safe        Complex     No
Learning curve  Hard        Medium      Easy
Data sharing    Easy        Locks,etc.  Pickle,queue
```

## When to Use Async

**Perfect for:**
- I/O-bound tasks (network, database, files)
- Handling many concurrent users
- WebSockets, streaming, long-lived connections
- Want simplicity and low overhead
- Single machine, single-threaded model

**Examples:**
- Web servers (FastAPI, aiohttp)
- Chat applications
- Real-time dashboards
- API clients calling multiple APIs
- Scrapers crawling many pages

**Code structure:**
```python
import asyncio
import httpx

async def fetch_url(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text

async def main():
    results = await asyncio.gather(
        fetch_url("https://example.com/1"),
        fetch_url("https://example.com/2"),
        fetch_url("https://example.com/3"),
    )

asyncio.run(main())
```

**Pros:**
- Lightweight
- Handles thousands of tasks easily
- Low memory overhead
- Simple, sequential-looking code
- Great for I/O-heavy work

**Cons:**
- Hard to learn
- Not for CPU-intensive work
- All tasks must be async
- Debugging is trickier
- Limited by GIL indirectly (not directly, since it's single-threaded)

---

## When to Use Threads

**Perfect for:**
- Lightweight I/O with legacy code
- Mixing sync and async (with caveats)
- Situations where async is not available

**Examples:**
- Python scripts using sync libraries
- Adding concurrency to existing projects without rewriting
- When you already have a thread-based architecture

**Code:**
```python
import threading
import requests
import time

def fetch_url(url):
    response = requests.get(url)  # Sync, but in a thread
    return response.text

threads = []
urls = [
    "https://example.com/1",
    "https://example.com/2",
    "https://example.com/3",
]

start = time.time()
for url in urls:
    t = threading.Thread(target=fetch_url, args=(url,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

end = time.time()
print(f"Time: {end - start:.2f}s")
```

**Why it works:** Each thread blocks on network I/O. OS switches between threads. Same total time as async, but higher overhead.

**Pros:**
- Works with existing sync libraries
- Easier to understand than async
- Can handle I/O-bound work

**Cons:**
- Higher memory per thread (~1-2 MB each)
- Harder to use (locks, race conditions)
- Not ideal for thousands of tasks
- Python GIL still limits parallel computation
- Context-switching overhead

---

## When to Use Multiprocessing

**Perfect for:**
- CPU-intensive work
- Using multiple cores
- True parallelism needed
- Process isolation important

**Examples:**
- Image processing pipeline
- Machine learning inference
- Data crunching
- Parallel batch processing

**Code:**
```python
import multiprocessing
import time

def cpu_intensive_task(n):
    result = 0
    for i in range(n):
        result += i ** 2
    return result

if __name__ == '__main__':
    with multiprocessing.Pool(4) as pool:
        results = pool.map(cpu_intensive_task, [10**7] * 4)
    print(results)
```

**Why it works:** Each process runs on a different CPU core. True parallelism.

**Pros:**
- True parallelism (multiple cores)
- Avoids GIL
- Process isolation
- Great for CPU-bound work

**Cons:**
- High memory overhead
- Slow startup
- Complex data sharing (pickling)
- Harder to debug
- Not for thousands of tasks

---

## Decision Tree: Which One to Use?

```
START
│
├─ Do you have I/O-bound tasks? (network, database, files)
│  │
│  ├─ YES
│  │  │
│  │  ├─ Can you rewrite as async?
│  │  │  ├─ YES → Use ASYNC ✓
│  │  │  └─ NO → Use THREADS
│  │  │
│  │  └─ How many concurrent tasks?
│  │     ├─ < 100 → Threads is fine
│  │     └─ > 100 → Async is better
│  │
│  └─ NO (CPU-bound work)
│     │
│     └─ Can you parallelize?
│        ├─ YES → Use MULTIPROCESSING ✓
│        └─ NO → Just use regular code
```

---

## Real-World Hybrid Approaches

### Async + Threads (Best of Both)

Sometimes you need to call a sync library from async:

```python
import asyncio
import requests

# Sync function
def fetch_sync(url):
    return requests.get(url).text

async def main():
    # Run sync function in a thread pool
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, fetch_sync, "https://example.com")
    print(result)

asyncio.run(main())
```

This lets you use async code while calling sync libraries.

### Async + Multiprocessing

For heavy computation + I/O:

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

def compute(n):
    # CPU-intensive
    return sum(i ** 2 for i in range(n))

async def main():
    loop = asyncio.get_event_loop()
    
    # Run in process pool
    with ProcessPoolExecutor(max_workers=4) as pool:
        results = await asyncio.gather(
            loop.run_in_executor(pool, compute, 10**7),
            loop.run_in_executor(pool, compute, 10**7),
            loop.run_in_executor(pool, compute, 10**7),
        )
    
    print(results)

asyncio.run(main())
```

---

## The Python GIL (Global Interpreter Lock)

This matters for threading:

**The GIL prevents multiple threads from executing Python bytecode simultaneously.**

This means:
- **Threading doesn't parallelize CPU work** in Python (unlike C/C++)
- **Threading IS useful for I/O work** (while one thread waits, OS can switch to another)
- **Multiprocessing avoids the GIL** (separate processes, separate GILs)

Example:

```python
import threading
import time

def cpu_work():
    total = 0
    for i in range(50_000_000):
        total += i ** 2
    return total

start = time.time()

# Single thread
cpu_work()
cpu_work()

end = time.time()
print(f"Sequential: {end - start:.2f}s")

start = time.time()

# Two threads (doesn't help because of GIL)
t1 = threading.Thread(target=cpu_work)
t2 = threading.Thread(target=cpu_work)
t1.start()
t2.start()
t1.join()
t2.join()

end = time.time()
print(f"Threaded: {end - start:.2f}s")  # About the same!
```

Both take about the same time because the GIL prevents parallel execution.

---

## Real-World Examples: Which to Use

### Example 1: Web API Server

```
Requirements: Handle 1,000 concurrent users, each making 1 database query

→ Use ASYNC (FastAPI)
   - I/O-bound (database)
   - Many concurrent users
   - Single process handles all

Result: Fast, simple, efficient
```

### Example 2: Image Processing Pipeline

```
Requirements: Process 10,000 images, each takes 1 second

→ Use MULTIPROCESSING
   - CPU-intensive
   - True parallelism on 8 cores: 10,000 / 8 = 1,250 seconds

Result: Uses all cores effectively
```

### Example 3: Legacy Code Needing Concurrency

```
Requirements: Existing sync library, need to handle 50 concurrent requests

→ Use THREADING
   - Can't rewrite to async (no async library available)
   - Not enough concurrency to cause major issues

Result: Works, some overhead but acceptable
```

### Example 4: Complex System

```
Requirements: Web server (I/O), image processing (CPU), long-lived connections (WebSocket)

→ Use ASYNC + MULTIPROCESSING
   - Main app: Async (FastAPI) for I/O and WebSockets
   - Heavy lifting: Multiprocessing workers for image processing
   - Communication: Async queue between them

Result: Handles all types of work efficiently
```

---

## Performance Comparison: Concrete Numbers

Fetching 100 URLs, each takes ~1 second:

| Approach | Time | Memory | Code Complexity |
|----------|------|--------|-----------------|
| Sequential | 100s | Low | Trivial |
| Async | ~1s | Low | Medium |
| Threads (10 at a time) | ~10s | Medium | Medium |
| Threads (100) | ~1s | High | High |
| Processes | ~1-2s | Very high | High |

**Async wins for this workload:** Fast, simple, low memory.

---

## Summary

- **Async**: Best for I/O-bound, many concurrent tasks, simple code
- **Threads**: Best when async unavailable, or lightweight concurrency needed
- **Multiprocessing**: Best for CPU-bound, true parallelism needed
- **GIL**: Prevents threads from parallelizing CPU work
- **Hybrid**: Mix async + threads, or async + processes for complex systems
- **Rule of thumb**: Default to async for I/O, multiprocessing for CPU

## Mental Model Takeaway

- **Async**: Conductor managing multiple musicians (I/O waits while others work)
- **Threads**: Referees managing multiple players (OS can interrupt mid-play)
- **Processes**: Separate games happening simultaneously (true parallelism)

## What You Should Now Understand

- When to use async vs threading vs multiprocessing
- Why async is superior for I/O-bound work
- Why threading doesn't parallelize CPU work in Python (GIL)
- How to combine multiple approaches
- The tradeoffs: memory, simplicity, performance, learning curve
- Real-world decision making

---

Next: Advanced async patterns—streaming, cancellation, timeouts, and building resilient async systems that don't break at scale.
