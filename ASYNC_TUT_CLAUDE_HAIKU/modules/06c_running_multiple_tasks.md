# Module 6c: Running Multiple Async Tasks Together — The Patterns of Concurrency

## The Key Patterns

Now that you understand `await` deeply, let's master the patterns for running multiple tasks concurrently. These patterns are the bread and butter of async programming.

## Pattern 1: Run All, Wait for All (`gather`)

This is the most common pattern:

```python
import asyncio

async def task(name, duration):
    print(f"{name} starting")
    await asyncio.sleep(duration)
    print(f"{name} done")
    return f"Result from {name}"

async def main():
    # Create tasks
    t1 = asyncio.create_task(task("Task 1", 2))
    t2 = asyncio.create_task(task("Task 2", 1))
    t3 = asyncio.create_task(task("Task 3", 3))
    
    # Wait for all
    results = await asyncio.gather(t1, t2, t3)
    print(f"All done! Results: {results}")

asyncio.run(main())
```

**Timeline:**
```
0.0s: All tasks start immediately
1.0s: Task 2 finishes
2.0s: Task 1 finishes
3.0s: Task 3 finishes, gather returns
Total: 3 seconds (the maximum duration)
```

**Use this when:**
- You have multiple independent tasks
- You want to wait for all of them to finish
- You don't care about the order they finish in

## Pattern 2: Run All from a List

If you have a dynamic list of tasks:

```python
async def main():
    tasks = [
        asyncio.create_task(task(f"Task {i}", i))
        for i in range(5)
    ]
    
    results = await asyncio.gather(*tasks)
    print(f"Results: {results}")

asyncio.run(main())
```

The `*tasks` unpacks the list into arguments for `gather()`.

**Shorthand version (even simpler):**

```python
async def main():
    # gather can create tasks automatically from coroutines
    results = await asyncio.gather(
        task("Task 1", 1),
        task("Task 2", 2),
        task("Task 3", 3),
    )
    print(f"Results: {results}")

asyncio.run(main())
```

## Pattern 3: Wait for the First One (`FIRST_COMPLETED`)

Sometimes you don't need all results. You just need the first:

```python
async def fetch_from_mirror(mirror_id, delay):
    await asyncio.sleep(delay)
    return f"Data from mirror {mirror_id}"

async def main():
    tasks = {
        asyncio.create_task(fetch_from_mirror(i, 2 - i * 0.5))
        for i in range(5)
    }
    
    # Whichever finishes first
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED
    )
    
    # Get the result
    result = done.pop().result()
    print(f"Got result first: {result}")
    
    # Cancel pending tasks (we don't need them anymore)
    for task in pending:
        task.cancel()

asyncio.run(main())
```

**Use this when:**
- You have redundant tasks (multiple mirrors, multiple databases)
- You want the fastest response
- You can ignore the rest

Timeline:
```
0.0s: All 5 tasks start
0.5s: Mirror 4 finishes first, returns result
Done: The other tasks are cancelled
Total: ~0.5 seconds
```

## Pattern 4: Wait for the First Exception

You might want to fail fast if any task fails:

```python
async def might_fail(task_id, should_fail=False):
    await asyncio.sleep(1)
    if should_fail:
        raise ValueError(f"Task {task_id} failed!")
    return f"Success from task {task_id}"

async def main():
    tasks = [
        asyncio.create_task(might_fail(1, False)),
        asyncio.create_task(might_fail(2, True)),   # This will fail
        asyncio.create_task(might_fail(3, False)),
    ]
    
    # Wait for the first to complete (done or failed)
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_EXCEPTION
    )
    
    # Check for exceptions
    for task in done:
        try:
            result = task.result()
            print(f"Got result: {result}")
        except Exception as e:
            print(f"Task failed: {e}")

asyncio.run(main())
```

## Pattern 5: Timeout on Multiple Tasks

If you want all tasks but with a timeout:

```python
async def slow_task(name, duration):
    print(f"{name} starting")
    await asyncio.sleep(duration)
    print(f"{name} done")
    return name

async def main():
    tasks = [
        asyncio.create_task(slow_task("Task 1", 2)),
        asyncio.create_task(slow_task("Task 2", 5)),  # This will timeout
        asyncio.create_task(slow_task("Task 3", 1)),
    ]
    
    try:
        results = await asyncio.wait_for(
            asyncio.gather(*tasks),
            timeout=3  # 3 second timeout for all
        )
    except asyncio.TimeoutError:
        print("Timed out waiting for all tasks!")
        # Cancel remaining tasks
        for task in tasks:
            task.cancel()

asyncio.run(main())
```

## Pattern 6: Sequential Within Concurrent

Sometimes you need some concurrency and some sequentiality:

```python
async def fetch(name, delay):
    print(f"Fetching {name}")
    await asyncio.sleep(delay)
    return f"Data: {name}"

async def process(data):
    print(f"Processing: {data}")
    await asyncio.sleep(0.5)
    return f"Processed: {data}"

async def main():
    # Step 1: Fetch from multiple sources concurrently
    fetch_results = await asyncio.gather(
        fetch("API 1", 1),
        fetch("API 2", 1),
        fetch("API 3", 1),
    )
    
    # Step 2: Process each sequentially (they depend on each other)
    for result in fetch_results:
        processed = await process(result)
        print(f"Got: {processed}")

asyncio.run(main())
```

Timeline:
```
0.0s: All 3 fetches start
1.0s: All 3 fetches done
1.0-1.5s: Process first
1.5-2.0s: Process second
2.0-2.5s: Process third
Total: 2.5 seconds
```

Without async, this would be:
- Fetch sequentially: 3 seconds
- Process sequentially: 1.5 seconds
- Total: 4.5 seconds

With async:
- Fetch concurrently: 1 second
- Process sequentially: 1.5 seconds
- Total: 2.5 seconds

## Pattern 7: Map Pattern (Run Same Task Multiple Times)

Common pattern—run the same async function on multiple inputs:

```python
async def process_item(item_id):
    print(f"Processing item {item_id}")
    await asyncio.sleep(1)
    return f"Item {item_id} processed"

async def main():
    item_ids = [1, 2, 3, 4, 5]
    
    # Create tasks for each item
    results = await asyncio.gather(*(
        process_item(item_id)
        for item_id in item_ids
    ))
    
    print(f"All processed: {results}")

asyncio.run(main())
```

Timeline:
```
0.0s: All 5 items start processing concurrently
1.0s: All done
Total: 1 second (not 5 seconds)
```

This is the async equivalent of multiprocessing's `Pool.map()`.

## Pattern 8: Stream Pattern (Process Results as They Arrive)

Instead of waiting for all, process each result as it completes:

```python
async def fetch(source_id, delay):
    print(f"Fetching from source {source_id}")
    await asyncio.sleep(delay)
    return f"Data from source {source_id}"

async def main():
    tasks = [
        asyncio.create_task(fetch(i, (5-i)*0.5))
        for i in range(5)
    ]
    
    # Process results as they complete, not in order
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"Got result: {result}")

asyncio.run(main())
```

Timeline:
```
0.0s: All tasks start
0.5s: Source 4 finishes, process it
1.0s: Source 3 finishes, process it
1.5s: Source 2 finishes, process it
2.0s: Source 1 finishes, process it
2.5s: Source 0 finishes, process it
Total: 2.5 seconds
```

Instead of waiting for the slowest, you process each as it arrives.

## Pattern 9: Cancellation

If you need to stop running tasks:

```python
async def long_task(name):
    try:
        for i in range(100):
            print(f"{name}: step {i}")
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        print(f"{name}: cancelled!")
        raise

async def main():
    task = asyncio.create_task(long_task("Task"))
    
    # Let it run for a bit
    await asyncio.sleep(0.3)
    
    # Cancel it
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("Task was cancelled")

asyncio.run(main())
```

Timeline:
```
0.0s: Task starts
0.1s: Step 0
0.2s: Step 1
0.3s: Step 2
0.3s: Cancellation requested
Task catches CancelledError and handles it
```

## Decision Tree: Which Pattern Should I Use?

```
Do you want...

→ All results, wait for all?
  Use: asyncio.gather()
  Pattern 1

→ First successful result only?
  Use: asyncio.wait(FIRST_COMPLETED)
  Pattern 3

→ First exception?
  Use: asyncio.wait(FIRST_EXCEPTION)
  Pattern 4

→ All results but with timeout?
  Use: asyncio.wait_for(gather())
  Pattern 5

→ Sequential steps each running concurrently?
  Use: gather() then await each
  Pattern 6

→ Run same function on multiple inputs?
  Use: gather with generator expression
  Pattern 7

→ Process results immediately as they arrive?
  Use: asyncio.as_completed()
  Pattern 8

→ Stop some tasks early?
  Use: task.cancel()
  Pattern 9
```

---

## Summary

- **`gather()`**: Run all, wait for all (most common)
- **`wait(FIRST_COMPLETED)`**: Get first successful result
- **`wait(FIRST_EXCEPTION)`**: Fail fast on first error
- **`wait_for()`**: Add timeout to any async operation
- **Sequential then concurrent**: gather() then await each result
- **`as_completed()`**: Process results as they arrive, not in order
- **`cancel()`**: Stop a running task

## Mental Model Takeaway

Think of these patterns as **coordination strategies**:

- `gather()`: "Do all these in parallel, then give me all the results"
- `FIRST_COMPLETED`: "Do all these, give me the fastest one"
- `as_completed()`: "Do all these, show me each one as it finishes"

Different problems need different coordination strategies.

## What You Should Now Understand

- How to run multiple async tasks concurrently
- The difference between gather() and wait()
- How to handle timeouts and cancellation
- How to process results as they arrive vs waiting for all
- When to use sequential vs concurrent execution
- The patterns that solve 90% of real-world async problems

---

Next: bugs, failures, and how to debug async code. Then FastAPI integration, threading comparison, and advanced topics.
