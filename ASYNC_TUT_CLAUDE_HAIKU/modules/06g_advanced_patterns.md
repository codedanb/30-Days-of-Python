# Module 6g: Advanced Patterns — Streaming, Cancellation, and Resilient Systems

## Going Deeper: Real-World Async Patterns

Now you understand the fundamentals. Let's explore patterns that make async systems robust and production-ready.

## Pattern 1: Streaming Responses

Instead of loading all data into memory, stream it:

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

async def generate_data():
    """Async generator that yields data"""
    for i in range(100):
        await asyncio.sleep(0.1)  # Simulate slow operation
        yield f"item {i}\n"

@app.get("/stream")
async def stream_data():
    return StreamingResponse(
        generate_data(),
        media_type="text/plain"
    )
```

**Why:** Large datasets don't fit in memory. Stream them instead.

**Timeline:**
```
Client connects
Server starts generator
0.0s: Item 0 sent
0.1s: Item 1 sent
0.2s: Item 2 sent
...
10.0s: Item 99 sent, done
Total: 10s, constant memory usage
```

Without streaming, you'd need to generate all 100 items first (slow to start).

## Pattern 2: Cancellation and Graceful Shutdown

When you need to stop async operations:

```python
import asyncio

async def long_running_task(task_id):
    try:
        for i in range(100):
            print(f"Task {task_id}: step {i}")
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        print(f"Task {task_id}: cancelled!")
        # Cleanup code here
        raise  # Important: re-raise to complete cancellation

async def main():
    task = asyncio.create_task(long_running_task(1))
    
    # Let it run for a bit
    await asyncio.sleep(0.5)
    
    # Cancel it
    print("Cancelling task...")
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("Task cancelled successfully")

asyncio.run(main())
```

**Output:**
```
Task 1: step 0
Task 1: step 1
Task 1: step 2
Task 1: step 3
Task 1: step 4
Cancelling task...
Task 1: cancelled!
Task cancelled successfully
```

**When you need this:**
- Shutdown (stop background workers gracefully)
- Timeouts (cancel slow operations)
- User requests (user closes connection)

## Pattern 3: Timeout with Fallback

Retry with exponential backoff:

```python
import asyncio
import httpx

async def fetch_with_timeout(url, retries=3):
    """Fetch with retry and exponential backoff"""
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await asyncio.wait_for(
                    client.get(url),
                    timeout=2.0  # 2 second timeout per attempt
                )
            return response.text
        except asyncio.TimeoutError:
            if attempt < retries - 1:
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                print(f"Timeout, retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)
            else:
                raise
        except Exception as e:
            print(f"Error: {e}")
            raise

async def main():
    try:
        result = await fetch_with_timeout("https://example.com/api")
        print(result)
    except asyncio.TimeoutError:
        print("All retries exhausted")

asyncio.run(main())
```

**Retry timeline:**
```
Attempt 1: timeout at 2s
Wait 1s
Attempt 2: timeout at 2s
Wait 2s
Attempt 3: timeout at 2s
Total: 2s + 1s + 2s + 2s + 2s = 9s
```

## Pattern 4: Rate Limiting with Semaphore

Limit concurrent operations:

```python
import asyncio

async def api_call(call_id, semaphore):
    """Make API call, but limit concurrency"""
    async with semaphore:  # Acquire permit
        print(f"Call {call_id}: starting")
        await asyncio.sleep(1)  # Simulate API call
        print(f"Call {call_id}: done")
        return call_id

async def main():
    semaphore = asyncio.Semaphore(3)  # Max 3 concurrent
    
    tasks = [
        asyncio.create_task(api_call(i, semaphore))
        for i in range(10)
    ]
    
    results = await asyncio.gather(*tasks)
    print(f"All done: {results}")

asyncio.run(main())
```

**Timeline (3 permits, 10 calls, each takes 1s):**
```
0.0s: Calls 0,1,2 start (uses all 3 permits)
1.0s: Calls 0,1,2 done, Calls 3,4,5 start
2.0s: Calls 3,4,5 done, Calls 6,7,8 start
3.0s: Calls 6,7,8 done, Call 9 starts
4.0s: Call 9 done
Total: 4 seconds
```

Without semaphore: All 10 run concurrently, might exceed API rate limits.

## Pattern 5: Queue-Based Concurrency

For producer-consumer patterns:

```python
import asyncio

async def producer(queue):
    """Produce items"""
    for i in range(5):
        print(f"Producer: creating item {i}")
        await queue.put(f"item {i}")
        await asyncio.sleep(0.1)
    
    # Signal that we're done
    await queue.put(None)

async def consumer(queue, consumer_id):
    """Consume items"""
    while True:
        item = await queue.get()
        
        if item is None:  # Sentinel value
            queue.task_done()
            break
        
        print(f"Consumer {consumer_id}: processing {item}")
        await asyncio.sleep(0.5)  # Process
        queue.task_done()

async def main():
    queue = asyncio.Queue()
    
    # One producer
    producer_task = asyncio.create_task(producer(queue))
    
    # Multiple consumers
    consumer_tasks = [
        asyncio.create_task(consumer(queue, i))
        for i in range(3)
    ]
    
    # Wait for all work to be done
    await asyncio.gather(producer_task, *consumer_tasks)
    print("All work done!")

asyncio.run(main())
```

**Timeline:**
```
0.0s: Producer creates item 0
0.1s: Producer creates item 1, Consumer 0 starts processing item 0
0.2s: Producer creates item 2, Consumer 1 starts processing item 1
...
Consumers work on items while producer keeps creating
Queue ensures work distribution
```

**Use cases:**
- Data pipelines (extract → transform → load)
- Task queues (worker systems)
- Backpressure handling

## Pattern 6: Monitoring and Health Checks

Background tasks that monitor system health:

```python
import asyncio
from fastapi import FastAPI

app = FastAPI()
app_state = {"healthy": True, "last_check": None}

async def health_monitor():
    """Run in background, check system health"""
    while True:
        try:
            await asyncio.sleep(5)  # Check every 5 seconds
            
            # Perform health checks
            is_healthy = await check_database()
            is_healthy = is_healthy and await check_api()
            
            app_state["healthy"] = is_healthy
            app_state["last_check"] = asyncio.get_event_loop().time()
            
        except Exception as e:
            print(f"Health check error: {e}")
            app_state["healthy"] = False

@app.on_event("startup")
async def startup():
    # Start background monitor
    asyncio.create_task(health_monitor())

@app.get("/health")
async def health():
    return {
        "healthy": app_state["healthy"],
        "last_check": app_state["last_check"],
    }

async def check_database():
    # Simulate database check
    return True

async def check_api():
    # Simulate API check
    return True
```

**Key points:**
- `@app.on_event("startup")` starts background tasks
- Monitor runs forever (in a loop)
- Main app endpoints can check status

## Pattern 7: Circuit Breaker

Prevent cascading failures:

```python
import asyncio
from enum import Enum
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = 1      # Normal operation
    OPEN = 2        # Failing, reject requests
    HALF_OPEN = 3   # Testing if recovered

class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    async def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            # Check if we should try to recover
            if (datetime.now() - self.last_failure_time).seconds > self.reset_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise
    
    def on_success(self):
        self.failures = 0
        self.state = CircuitState.CLOSED
    
    def on_failure(self):
        self.failures += 1
        self.last_failure_time = datetime.now()
        if self.failures >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Usage
breaker = CircuitBreaker(failure_threshold=3)

async def unstable_api():
    # Sometimes fails
    import random
    if random.random() < 0.7:  # 70% failure rate
        raise Exception("API error")
    return "success"

async def main():
    for i in range(20):
        try:
            result = await breaker.call(unstable_api)
            print(f"Call {i}: {result}")
        except Exception as e:
            print(f"Call {i}: {e} ({breaker.state.name})")
        
        await asyncio.sleep(0.1)

asyncio.run(main())
```

**States:**
- **CLOSED**: Normal, all requests go through
- **OPEN**: Too many failures, reject requests immediately (fast fail)
- **HALF_OPEN**: Timeout passed, test if service recovered

## Pattern 8: Exponential Backoff with Jitter

Prevent thundering herd:

```python
import asyncio
import random

async def call_with_backoff(func, max_retries=5):
    """Retry with exponential backoff and jitter"""
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            # Exponential backoff + random jitter
            base_wait = 2 ** attempt
            jitter = random.uniform(0, base_wait * 0.1)  # 10% jitter
            wait_time = base_wait + jitter
            
            print(f"Attempt {attempt + 1} failed, waiting {wait_time:.2f}s...")
            await asyncio.sleep(wait_time)

async def unreliable_api():
    import random
    if random.random() < 0.8:
        raise Exception("API error")
    return "success"

async def main():
    result = await call_with_backoff(unreliable_api)
    print(f"Success: {result}")

asyncio.run(main())
```

**Why jitter:** If many clients retry at the same time, they all hammer the server simultaneously (thundering herd). Jitter spreads them out.

## Pattern 9: Bulkhead Isolation

Isolate resource pools to prevent one failure from taking down everything:

```python
import asyncio

class BulkheadPool:
    def __init__(self, max_concurrent=5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def execute(self, func, *args, **kwargs):
        async with self.semaphore:
            return await func(*args, **kwargs)

# Separate pools for different services
api_pool = BulkheadPool(max_concurrent=10)
db_pool = BulkheadPool(max_concurrent=5)

async def api_call():
    async with asyncio.timeout(2):
        return await api_pool.execute(external_api_call)

async def db_call():
    async with asyncio.timeout(5):
        return await db_pool.execute(database_query)

async def external_api_call():
    await asyncio.sleep(1)
    return "api response"

async def database_query():
    await asyncio.sleep(0.5)
    return "db response"
```

**Why:** If API calls are slow, they don't block database queries (separate bulkheads).

---

## Summary of Advanced Patterns

| Pattern | Use Case | Complexity |
|---------|----------|-----------|
| Streaming | Large responses | Low |
| Cancellation | Graceful shutdown | Medium |
| Timeout + Retry | Unreliable services | Medium |
| Semaphore | Rate limiting | Low |
| Queues | Producer-consumer | Medium |
| Monitoring | System health | Medium |
| Circuit breaker | Failure prevention | High |
| Backoff + Jitter | Preventing thundering herd | Medium |
| Bulkhead | Isolation | High |

## Mental Model Takeaway

Think of a robust async system as an **airport**:

- **Streaming**: Passengers board while others are still checking in (don't wait for everyone)
- **Cancellation**: Gates close, last passenger can exit (graceful shutdown)
- **Timeout + Retry**: Delayed flight, some people rebook (resilience)
- **Semaphore**: Only 5 people at a time at each gate (rate limit)
- **Queues**: Check-in desk, security, gates—orderly flow (pipeline)
- **Circuit breaker**: Close gate if too many missed flights (fail fast)
- **Bulkhead**: Separate terminals so one delay doesn't affect others (isolation)

## What You Should Now Understand

- How to stream responses without loading everything into memory
- How to gracefully cancel async operations
- How to retry with exponential backoff and jitter
- How to limit concurrency with semaphores
- How to coordinate work with queues
- How to monitor system health
- How to prevent cascading failures (circuit breaker)
- How to prevent resource exhaustion (bulkhead isolation)
- That production systems need more than just async—they need resilience patterns

---

You've now completed the comprehensive async journey. From first principles to production-ready patterns. Next: practical code examples and the comprehensive README that ties it all together.
