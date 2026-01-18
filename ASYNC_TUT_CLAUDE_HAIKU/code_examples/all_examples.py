#!/usr/bin/env python3
"""
Async Programming: Complete Code Examples

This file contains runnable code examples organized by module. Copy and run them!
"""

# =============================================================================
# MODULE 6a: YOUR FIRST ASYNC PROGRAM
# =============================================================================

# Example 1: Basic Async Function
# --------------------------------
import asyncio

async def hello():
    print("Hello!")
    return 42

# Run it
# result = asyncio.run(hello())
# print(f"Result: {result}")


# Example 2: Using `await` and Sleep
# ------------------------------------
async def greet(name):
    print(f"Hello, {name}!")
    await asyncio.sleep(2)
    print(f"Goodbye, {name}!")

# Run it
# asyncio.run(greet("Alice"))


# Example 3: Multiple Concurrent Tasks
# ------------------------------------
async def greet_multi(name, delay):
    print(f"Hello, {name}!")
    await asyncio.sleep(delay)
    print(f"Goodbye, {name}!")

async def main_concurrent():
    # Create tasks
    task1 = asyncio.create_task(greet_multi("Alice", 2))
    task2 = asyncio.create_task(greet_multi("Bob", 1))
    
    # Wait for both
    await asyncio.gather(task1, task2)

# Run it
# asyncio.run(main_concurrent())


# Example 4: Synchronous vs Asynchronous Comparison
# --------------------------------------------------
import time

# SYNCHRONOUS (slow)
def fetch_sync(url, delay=1):
    time.sleep(delay)  # Blocking
    return f"Data from {url}"

def fetch_three_sync():
    start = time.time()
    result1 = fetch_sync("api1.com")
    result2 = fetch_sync("api2.com")
    result3 = fetch_sync("api3.com")
    elapsed = time.time() - start
    print(f"Sync took {elapsed:.2f}s")
    return [result1, result2, result3]

# ASYNCHRONOUS (fast)
async def fetch_async(url, delay=1):
    await asyncio.sleep(delay)  # Non-blocking
    return f"Data from {url}"

async def fetch_three_async():
    start = time.time()
    results = await asyncio.gather(
        fetch_async("api1.com"),
        fetch_async("api2.com"),
        fetch_async("api3.com")
    )
    elapsed = time.time() - start
    print(f"Async took {elapsed:.2f}s")
    return results

# Run them
# fetch_three_sync()      # Takes ~3 seconds
# asyncio.run(fetch_three_async())  # Takes ~1 second


# Example 5: API Fetching Simulation (5 URLs)
# -------------------------------------------
async def fetch_url(session, url, delay=0.5):
    """Simulate fetching a URL"""
    await asyncio.sleep(delay)
    return f"Content from {url}"

async def fetch_all_urls():
    urls = [
        "https://api.github.com",
        "https://api.twitter.com",
        "https://api.stripe.com",
        "https://openai.api.com",
        "https://docs.python.org"
    ]
    
    # Fetch all concurrently
    results = await asyncio.gather(
        *[fetch_url(None, url) for url in urls]
    )
    
    for result in results:
        print(result)

# Run it
# asyncio.run(fetch_all_urls())


# =============================================================================
# MODULE 6b: UNDERSTANDING AWAIT
# =============================================================================

# Example 1: What await Does (Pauses and Resumes)
# -----------------------------------------------
async def task1():
    print("Task1: Starting")
    await asyncio.sleep(2)
    print("Task1: Done")

async def task2():
    print("Task2: Starting")
    await asyncio.sleep(1)
    print("Task2: Done")

async def demo_await():
    print("--- Sequential (one after another) ---")
    await task1()
    await task2()
    # Takes ~3 seconds
    
    print("\n--- Concurrent (at the same time) ---")
    await asyncio.gather(task1(), task2())
    # Takes ~2 seconds

# Run it
# asyncio.run(demo_await())


# Example 2: forgetting await (WRONG!)
# ------------------------------------
async def example_wrong():
    # This creates a coroutine but doesn't run it
    coro = greet("Alice")  # WRONG: not awaited
    print(coro)  # Prints: <coroutine object greet at 0x...>

# The coroutine never runs!
# asyncio.run(example_wrong())


# Example 3: Correct way (with await)
# -----------------------------------
async def example_right():
    # This runs the coroutine
    result = await greet("Alice")  # CORRECT: awaited
    print(f"Completed: {result}")

# asyncio.run(example_right())


# Example 4: Contagion - once async, always async
# -----------------------------------------------
async def function_a():
    await asyncio.sleep(1)
    return "A done"

async def function_b():
    result = await function_a()  # Must await because A is async
    return f"B: {result}"

async def function_c():
    result = await function_b()  # Must await because B is async
    return f"C: {result}"

# C must be run with asyncio.run (because it's async)
# output = asyncio.run(function_c())


# Example 5: Common Pitfall - Missing await Creates Race Condition
# ---------------------------------------------------------------
async def task_a():
    await asyncio.sleep(1)
    print("Task A done")

async def task_b():
    await asyncio.sleep(1)
    print("Task B done")

async def wrong_race():
    # WRONG: task_a() returns coroutine, never runs
    asyncio.create_task(task_a())  # Fire and forget (implicit)
    await task_b()
    # Task A might not complete before program ends

async def right_race():
    # RIGHT: properly track both tasks
    t1 = asyncio.create_task(task_a())
    t2 = asyncio.create_task(task_b())
    await asyncio.gather(t1, t2)

# asyncio.run(right_race())


# =============================================================================
# MODULE 6c: RUNNING MULTIPLE TASKS
# =============================================================================

# Example 1: gather() - Wait for All Tasks
# ----------------------------------------
async def fetch_data(item_id, delay):
    await asyncio.sleep(delay)
    return f"Data for item {item_id}"

async def demo_gather():
    # Start all tasks concurrently
    results = await asyncio.gather(
        fetch_data(1, 2),
        fetch_data(2, 1),
        fetch_data(3, 3),
    )
    print(results)
    # Output: ['Data for item 1', 'Data for item 2', 'Data for item 3']

# asyncio.run(demo_gather())


# Example 2: gather() with Return_exceptions
# -------------------------------------------
async def fetch_maybe_fails(item_id, delay, fails=False):
    await asyncio.sleep(delay)
    if fails:
        raise ValueError(f"Failed for {item_id}")
    return f"Data for {item_id}"

async def demo_gather_exceptions():
    results = await asyncio.gather(
        fetch_maybe_fails(1, 1, fails=False),
        fetch_maybe_fails(2, 1, fails=True),
        fetch_maybe_fails(3, 1, fails=False),
        return_exceptions=True,  # Don't raise, return exceptions
    )
    print(results)
    # Output: ['Data for 1', ValueError('Failed for 2'), 'Data for 3']

# asyncio.run(demo_gather_exceptions())


# Example 3: wait(FIRST_COMPLETED) - Race Tasks
# -----------------------------------------------
async def demo_first_completed():
    tasks = [
        asyncio.create_task(fetch_data(1, 3)),
        asyncio.create_task(fetch_data(2, 1)),
        asyncio.create_task(fetch_data(3, 2)),
    ]
    
    while tasks:
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        
        for task in done:
            print(f"Completed: {task.result()}")
        
        tasks = list(pending)

# asyncio.run(demo_first_completed())


# Example 4: as_completed() - Process as Done
# -------------------------------------------
async def demo_as_completed():
    tasks = [
        fetch_data(1, 3),
        fetch_data(2, 1),
        fetch_data(3, 2),
    ]
    
    # Process in completion order
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"Got: {result}")

# asyncio.run(demo_as_completed())


# Example 5: Timeout Pattern
# --------------------------
async def slow_task():
    await asyncio.sleep(10)
    return "Done!"

async def demo_timeout():
    try:
        result = await asyncio.wait_for(slow_task(), timeout=2)
        print(result)
    except asyncio.TimeoutError:
        print("Task took too long!")

# asyncio.run(demo_timeout())


# Example 6: Semaphore - Limit Concurrent Tasks
# -----------------------------------------------
async def limited_fetch(semaphore, item_id, delay):
    async with semaphore:
        print(f"Fetching {item_id}...")
        await asyncio.sleep(delay)
        print(f"Done {item_id}")
        return f"Data {item_id}"

async def demo_semaphore():
    semaphore = asyncio.Semaphore(2)  # Max 2 concurrent
    
    tasks = [
        limited_fetch(semaphore, i, 1)
        for i in range(5)
    ]
    
    results = await asyncio.gather(*tasks)
    return results

# asyncio.run(demo_semaphore())


# =============================================================================
# MODULE 6d: COMMON BUGS & DEBUGGING
# =============================================================================

# Bug 1: Forgetting await
# -----------------------
async def buggy_forgot_await():
    coro = greet("Alice")  # BUG: Created but not awaited
    # Coroutine never runs!

# Fixed:
async def fixed_forgot_await():
    result = await greet("Alice")  # FIXED: Awaited
    return result


# Bug 2: Race Condition - Task Lost
# ---------------------------------
async def buggy_lost_task():
    asyncio.create_task(fetch_data(1, 2))  # BUG: Created but not awaited
    # Task might not complete before function ends

# Fixed:
async def fixed_lost_task():
    task = asyncio.create_task(fetch_data(1, 2))
    await task  # FIXED: Properly awaited


# Bug 3: Blocking the Event Loop
# --------------------------------
async def buggy_blocking():
    # BUG: Blocks entire event loop for 2 seconds!
    time.sleep(2)
    return "Done"

# Fixed:
async def fixed_blocking():
    # FIXED: Non-blocking, yields to event loop
    await asyncio.sleep(2)
    return "Done"


# Bug 4: Race Condition - Shared State
# ------------------------------------
counter = 0

async def buggy_increment():
    global counter
    # BUG: Race condition!
    current = counter
    await asyncio.sleep(0.1)  # Yield point - other tasks can run
    counter = current + 1

async def buggy_race():
    await asyncio.gather(
        buggy_increment(),
        buggy_increment(),
        buggy_increment(),
    )
    print(f"Counter: {counter}")  # Prints 1 instead of 3!


# Fixed with Lock:
async def fixed_increment():
    global counter
    async with asyncio.Lock():  # FIXED: Use lock
        current = counter
        await asyncio.sleep(0.1)
        counter = current + 1


# Bug 5: Uncaught Exception Silently Fails
# ----------------------------------------
async def buggy_exception():
    task = asyncio.create_task(greet("Alice"))
    # BUG: If greet raises, exception is never seen

# Fixed:
async def fixed_exception():
    task = asyncio.create_task(greet("Alice"))
    try:
        result = await task  # FIXED: Await to catch exceptions
    except Exception as e:
        print(f"Error: {e}")


# =============================================================================
# MODULE 6e: FASTAPI AND WEB SERVERS
# =============================================================================

# Example 1: Basic FastAPI Async Endpoint
# -----------------------------------------------
# Note: These require FastAPI installed: pip install fastapi uvicorn

# from fastapi import FastAPI
# import asyncio
# 
# app = FastAPI()
# 
# @app.get("/")
# async def read_root():
#     await asyncio.sleep(1)  # Simulated I/O
#     return {"message": "Hello, World!"}
# 
# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     await asyncio.sleep(0.5)  # Simulated database query
#     return {"item_id": item_id, "name": f"Item {item_id}"}
# 
# # Run with: uvicorn main:app --reload


# Example 2: Concurrent API Calls Within Endpoint
# -----------------------------------------------
# from fastapi import FastAPI
# import httpx
# 
# app = FastAPI()
# 
# async def fetch_from_service(client, url):
#     response = await client.get(url)
#     return response.json()
# 
# @app.get("/combined")
# async def get_combined():
#     async with httpx.AsyncClient() as client:
#         # Fetch from 3 services concurrently
#         results = await asyncio.gather(
#             fetch_from_service(client, "https://api.service1.com/data"),
#             fetch_from_service(client, "https://api.service2.com/data"),
#             fetch_from_service(client, "https://api.service3.com/data"),
#         )
#     return {"services": results}


# Example 3: Background Tasks
# -----------------------------------------------
# from fastapi import FastAPI, BackgroundTasks
# import asyncio
# 
# app = FastAPI()
# 
# async def log_request(request_id):
#     await asyncio.sleep(1)  # Simulated async logging
#     print(f"Logged request {request_id}")
# 
# @app.post("/process")
# async def process(background_tasks: BackgroundTasks):
#     background_tasks.add_task(log_request, "req-123")
#     return {"status": "processing"}


# =============================================================================
# MODULE 6f: ASYNC VS THREADS VS PROCESSES
# =============================================================================

# Example 1: Async vs Threads for I/O-bound Work
# -----------------------------------------------
from concurrent.futures import ThreadPoolExecutor

# ASYNC version
async def io_task_async(task_id):
    await asyncio.sleep(1)
    return f"Async task {task_id} done"

async def main_async():
    start = time.time()
    results = await asyncio.gather(
        *[io_task_async(i) for i in range(5)]
    )
    elapsed = time.time() - start
    print(f"Async 5 tasks: {elapsed:.2f}s")

# THREADS version
def io_task_thread(task_id):
    time.sleep(1)
    return f"Thread task {task_id} done"

def main_threads():
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        list(executor.map(io_task_thread, range(5)))
    elapsed = time.time() - start
    print(f"Threads 5 tasks: {elapsed:.2f}s")

# Run both
# asyncio.run(main_async())      # Takes ~1 second
# main_threads()                 # Takes ~1 second
# Both are fast for I/O, but async uses less memory


# Example 2: CPU-bound Work (Where Multiprocessing Wins)
# -----------------------------------------------
from multiprocessing import Pool

def cpu_task(n):
    """Compute fibonacci - CPU bound"""
    if n <= 1:
        return n
    return cpu_task(n - 1) + cpu_task(n - 2)

def main_cpu_sync():
    start = time.time()
    results = [cpu_task(30) for _ in range(4)]
    elapsed = time.time() - start
    print(f"Sequential CPU: {elapsed:.2f}s")

def main_cpu_threads():
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(cpu_task, [30] * 4))
    elapsed = time.time() - start
    print(f"Threads CPU: {elapsed:.2f}s (NO speedup due to GIL)")

def main_cpu_multiprocess():
    start = time.time()
    with Pool(4) as pool:
        pool.map(cpu_task, [30] * 4)
    elapsed = time.time() - start
    print(f"Multiprocessing CPU: {elapsed:.2f}s (Real speedup!)")

# Run all
# main_cpu_sync()              # Takes ~60 seconds (slowest)
# main_cpu_threads()           # Takes ~60 seconds (GIL blocks parallelism)
# main_cpu_multiprocess()      # Takes ~15 seconds (4x faster!)


# =============================================================================
# MODULE 6g: ADVANCED PATTERNS
# =============================================================================

# Pattern 1: Streaming/Chunked Responses
# ----------------------------------------
async def stream_data():
    """Yield data in chunks"""
    for i in range(5):
        await asyncio.sleep(0.5)
        yield f"Chunk {i}\n"

async def demo_streaming():
    async for chunk in stream_data():
        print(chunk, end="")

# asyncio.run(demo_streaming())


# Pattern 2: Cancellation
# -----------------------
async def long_task():
    try:
        for i in range(10):
            print(f"Task step {i}")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Task was cancelled!")
        raise  # Re-raise to signal cancellation

async def demo_cancellation():
    task = asyncio.create_task(long_task())
    
    await asyncio.sleep(3)
    task.cancel()  # Cancel after 3 seconds
    
    try:
        await task
    except asyncio.CancelledError:
        print("Caught cancellation")

# asyncio.run(demo_cancellation())


# Pattern 3: Timeout with Retry
# ------------------------------
async def unreliable_api(attempt):
    """Might fail or be slow"""
    await asyncio.sleep(1)
    if attempt < 2:
        raise ValueError("API error")
    return f"Success on attempt {attempt}"

async def retry_with_timeout(max_retries=3, timeout=2):
    for attempt in range(1, max_retries + 1):
        try:
            result = await asyncio.wait_for(
                unreliable_api(attempt),
                timeout=timeout
            )
            return result
        except asyncio.TimeoutError:
            print(f"Attempt {attempt}: Timeout")
        except ValueError as e:
            print(f"Attempt {attempt}: {e}")
    
    raise ValueError("All retries exhausted")

# asyncio.run(retry_with_timeout())


# Pattern 4: Rate Limiting with Semaphore
# ----------------------------------------
class RateLimiter:
    def __init__(self, max_requests=10, window=1.0):
        self.max_requests = max_requests
        self.window = window
        self.semaphore = asyncio.Semaphore(max_requests)
    
    async def acquire(self):
        async with self.semaphore:
            yield

async def rate_limited_request(limiter, request_id):
    async with limiter.semaphore:
        print(f"Request {request_id} executing")
        await asyncio.sleep(0.1)
        print(f"Request {request_id} done")

async def demo_rate_limiter():
    limiter = RateLimiter(max_requests=3)
    
    tasks = [
        rate_limited_request(limiter, i)
        for i in range(10)
    ]
    
    await asyncio.gather(*tasks)

# asyncio.run(demo_rate_limiter())


# Pattern 5: Producer-Consumer Queue
# ----------------------------------
async def producer(queue):
    for i in range(5):
        await asyncio.sleep(0.5)
        await queue.put(f"Item {i}")
        print(f"Produced: Item {i}")

async def consumer(queue):
    while True:
        item = await queue.get()
        print(f"Consuming: {item}")
        queue.task_done()

async def demo_queue():
    queue = asyncio.Queue()
    
    # Start producer and consumers
    producer_task = asyncio.create_task(producer(queue))
    consumer_tasks = [
        asyncio.create_task(consumer(queue))
        for _ in range(2)
    ]
    
    # Wait for producer to finish
    await producer_task
    await queue.join()
    
    # Cancel consumers
    for task in consumer_tasks:
        task.cancel()
    
    await asyncio.gather(*consumer_tasks, return_exceptions=True)

# asyncio.run(demo_queue())


# Pattern 6: Health Monitoring
# ----------------------------
async def monitored_task(task_id):
    for i in range(5):
        await asyncio.sleep(1)
        print(f"Task {task_id}: step {i}")

async def health_check():
    """Periodically check if tasks are running"""
    while True:
        await asyncio.sleep(2)
        print("Health check: All tasks running")

async def demo_health():
    tasks = [
        asyncio.create_task(monitored_task(i))
        for i in range(3)
    ]
    
    health_task = asyncio.create_task(health_check())
    
    await asyncio.gather(*tasks)
    health_task.cancel()

# asyncio.run(demo_health())


# Pattern 7: Circuit Breaker
# --------------------------
class CircuitBreaker:
    def __init__(self, failure_threshold=3, timeout=5):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    async def call(self, func, *args):
        if self.state == "OPEN":
            if time.time() - self.last_failure > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit is OPEN")
        
        try:
            result = await func(*args)
            self.failures = 0
            self.state = "CLOSED"
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure = time.time()
            if self.failures >= self.failure_threshold:
                self.state = "OPEN"
            raise


# Pattern 8: Bulkhead Isolation (Separate Pools)
# -----------------------------------------------
class BulkheadPool:
    def __init__(self, max_concurrent=5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def execute(self, coro):
        async with self.semaphore:
            return await coro

async def isolated_work(bulkhead, work_id):
    async def work():
        print(f"Work {work_id} starting")
        await asyncio.sleep(1)
        print(f"Work {work_id} done")
    
    return await bulkhead.execute(work())


# Pattern 9: Exponential Backoff Retry
# ------------------------------------
async def flaky_api():
    """Fails 50% of the time"""
    import random
    await asyncio.sleep(0.1)
    if random.random() < 0.5:
        raise ValueError("API error")
    return "Success"

async def retry_exponential(max_retries=5, base_delay=0.1):
    for attempt in range(max_retries):
        try:
            return await flaky_api()
        except ValueError:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s")
                await asyncio.sleep(delay)
    
    raise ValueError("All retries exhausted")

# asyncio.run(retry_exponential())


if __name__ == "__main__":
    print("Async Programming Examples")
    print("=" * 50)
    print("\nThis file contains examples for each module.")
    print("Uncomment the examples you want to run.")
    print("\nExample usage:")
    print("  asyncio.run(demo_gather())")
    print("  asyncio.run(demo_timeout())")
