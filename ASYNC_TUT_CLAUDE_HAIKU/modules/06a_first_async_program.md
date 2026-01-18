# Module 6a: Your First Async Program — Write and Understand Real Code

## Now We Code

You understand the concepts. You understand how the event loop works. Now let's write real Python code.

Don't rush through this. Type out every example. Run it. Break it. Fix it. The goal is not just to see async code, but to **feel** how it works.

## The Setup

First, let's make sure you have Python and the right libraries. Python 3.7+ has `asyncio` built in, which is the main async library.

```bash
python --version  # Should be 3.7 or higher
```

We'll use Python's `asyncio` library. It comes with Python, so no installation needed.

## Example 1: Your Absolute First Async Function

Let me start with the simplest possible async program:

```python
import asyncio

async def hello():
    print("Hello!")
    return 42

# Run the async function
result = asyncio.run(hello())
print(f"Result: {result}")
```

**Let's understand this line by line:**

**`import asyncio`**: This is Python's built-in async library. It has the event loop and utilities for async programming.

**`async def hello():`**: The `async` keyword means "this is an async function." It can use `await` inside it and is designed to be scheduled by the event loop.

**`asyncio.run(hello())`**: This:
1. Creates an event loop
2. Runs the async function
3. Cleans up the event loop
4. Returns the result

**What happens when you run this:**
1. The event loop starts
2. `hello()` is scheduled as a task
3. `hello()` prints "Hello!"
4. `hello()` returns 42
5. The event loop exits
6. 42 is printed

**Key insight**: There's nothing async happening here. No awaiting. No waiting. It's sequential. This is just a function that's wrapped in async syntax. But it's important to see that async syntax doesn't require concurrency.

## Example 2: Using `await` and Time

Now let's introduce waiting:

```python
import asyncio
import time

async def greet(name):
    print(f"Hello, {name}!")
    await asyncio.sleep(2)  # Wait for 2 seconds
    print(f"Goodbye, {name}!")

# Run a single async function
asyncio.run(greet("Alice"))
```

**What's new:**

**`await asyncio.sleep(2)`**: This:
- Pauses the function for 2 seconds
- Gives control back to the event loop
- The event loop can run other tasks during these 2 seconds
- After 2 seconds, resumes the function

**What happens:**
1. Prints "Hello, Alice!"
2. Waits 2 seconds (during this time, event loop is idle because there's only one task)
3. Prints "Goodbye, Alice!"
4. Done

Total time: ~2 seconds (as expected, since we have only one task and it waits for 2 seconds).

**This looks exactly like synchronous code!** And it is, functionally. But notice the `await` keyword. That's what makes it async. It says "I'm about to wait for something."

## Example 3: Multiple Tasks — The Concurrency Happens Here

Now the interesting part:

```python
import asyncio

async def greet(name, delay):
    print(f"Hello, {name}!")
    await asyncio.sleep(delay)
    print(f"Goodbye, {name}!")

async def main():
    # Create two tasks
    task1 = asyncio.create_task(greet("Alice", 2))
    task2 = asyncio.create_task(greet("Bob", 1))
    
    # Wait for both to complete
    await asyncio.gather(task1, task2)

asyncio.run(main())
```

**What's new:**

**`asyncio.create_task(...)`**: This schedules the async function as a task. It doesn't run it immediately—it puts it in the event loop's queue.

**`asyncio.gather(task1, task2)`**: This waits for both tasks to complete. It's the event loop's way of saying "run these tasks concurrently."

**What happens (the timeline):**
```
Time: 0.0s
  - task1 starts: prints "Hello, Alice!"
  - task1 hits await asyncio.sleep(2), pauses
  
Time: 0.01s (roughly)
  - task2 starts: prints "Hello, Bob!"
  - task2 hits await asyncio.sleep(1), pauses
  
Time: 1.0s
  - task2's sleep is done
  - task2 resumes: prints "Goodbye, Bob!"
  - task2 is done
  
Time: 2.0s
  - task1's sleep is done
  - task1 resumes: prints "Goodbye, Alice!"
  - task1 is done
  
Done

Total time: ~2 seconds (not 3 seconds)
```

**Run this and notice:**
- Both "Hello" messages print immediately (about the same time)
- "Goodbye, Bob!" prints after 1 second
- "Goodbye, Alice!" prints after 2 seconds
- Total time is about 2 seconds (not 3)

This is **concurrency in action**. Two tasks running, but only 2 seconds of actual waiting (the maximum), not 3 seconds (the sum).

## Example 4: More Realistic — Simulating API Calls

Let's simulate something real: calling APIs:

```python
import asyncio
import random

async def fetch_data(source_id, delay):
    """Simulate fetching data from an API"""
    print(f"Fetching data from source {source_id}...")
    await asyncio.sleep(delay)  # Simulate network delay
    result = f"Data from source {source_id}"
    print(f"Received: {result}")
    return result

async def main():
    print("Starting requests...")
    start_time = asyncio.get_event_loop().time()
    
    # Fetch from 5 sources
    sources = [1, 2, 3, 4, 5]
    delays = [2, 1, 3, 1, 2]  # Different delays for each source
    
    # Create all tasks
    tasks = [
        asyncio.create_task(fetch_data(source_id, delay))
        for source_id, delay in zip(sources, delays)
    ]
    
    # Wait for all to complete
    results = await asyncio.gather(*tasks)
    
    end_time = asyncio.get_event_loop().time()
    total_time = end_time - start_time
    
    print(f"\nAll done!")
    print(f"Results: {results}")
    print(f"Total time: {total_time:.2f} seconds")

asyncio.run(main())
```

**Key learnings from this:**

**`asyncio.create_task(...)`** creates a task that starts immediately (in the background).

**`*tasks` unpacks the list** into arguments for `gather()`.

**`asyncio.gather(*tasks)` waits for all tasks**.

**What you'll see:**
- All 5 "Fetching..." messages print almost immediately (all tasks start)
- Responses come back in order of their delays (1s, 1s, 2s, 2s, 3s)
- Total time is ~3 seconds (the max delay), not 9 seconds (the sum of delays)

This is the power of async. 5 tasks, 9 seconds of waiting, but completed in 3 seconds.

## Example 5: Understanding the Difference - Sync vs Async

Let me show you the same program written synchronously:

**Synchronous version** (blocking):
```python
import time

def fetch_data_sync(source_id, delay):
    print(f"Fetching data from source {source_id}...")
    time.sleep(delay)  # This blocks everything
    result = f"Data from source {source_id}"
    print(f"Received: {result}")
    return result

print("Starting requests...")
start_time = time.time()

sources = [1, 2, 3, 4, 5]
delays = [2, 1, 3, 1, 2]

results = []
for source_id, delay in zip(sources, delays):
    result = fetch_data_sync(source_id, delay)
    results.append(result)

end_time = time.time()
total_time = end_time - start_time

print(f"\nAll done!")
print(f"Results: {results}")
print(f"Total time: {total_time:.2f} seconds")
```

**What you'll see:**
- One "Fetching..." message at a time
- One response at a time (waiting for each)
- Total time: 9 seconds (sum of all delays)

**Compare:**
- **Synchronous**: 9 seconds (2 + 1 + 3 + 1 + 2)
- **Async**: ~3 seconds (max of 3)

Same work, same operations, **3x faster** because the async version doesn't waste time waiting sequentially.

## Common Async Patterns

Now that you've seen the basics, here are patterns you'll use constantly:

### Pattern 1: Create and Run Tasks

```python
async def main():
    task1 = asyncio.create_task(do_something())
    task2 = asyncio.create_task(do_something_else())
    
    # Wait for both
    result1, result2 = await asyncio.gather(task1, task2)
```

### Pattern 2: Sequential Async (Do One, Then the Next)

```python
async def main():
    result1 = await do_something()
    result2 = await do_something_else()  # Waits for first to finish
```

Notice: No `create_task()`. Just `await` directly. This is sequential, not concurrent.

### Pattern 3: Waiting for the First to Complete

```python
async def main():
    task1 = asyncio.create_task(do_something())
    task2 = asyncio.create_task(do_something_else())
    
    # Whichever finishes first
    done, pending = await asyncio.wait(
        [task1, task2],
        return_when=asyncio.FIRST_COMPLETED
    )
```

### Pattern 4: Timeout

```python
async def main():
    try:
        result = await asyncio.wait_for(
            fetch_data(),
            timeout=5.0  # Raise error if takes more than 5 seconds
        )
    except asyncio.TimeoutError:
        print("Request timed out!")
```

## A Critical Mind Shift: Thinking in Tasks, Not Functions

Here's the insight that changes how you write async code:

When you write sync code:
```python
def main():
    result1 = function_a()  # Runs, returns
    result2 = function_b()  # Runs, returns
    return result1 + result2
```

You think: "Do A, then do B."

When you write async code:
```python
async def main():
    task1 = asyncio.create_task(function_a())  # Starts
    task2 = asyncio.create_task(function_b())  # Starts
    result1, result2 = await asyncio.gather(task1, task2)  # Wait for both
    return result1 + result2
```

You're thinking differently: "Start both, then wait for both to finish."

This is the paradigm shift. You're no longer thinking "sequential steps" but "concurrent tasks."

## A Word of Warning: Debugging Async Code

Before you go wild, understand: **Debugging async code is harder than sync code.**

When something breaks:
- You might not see where it broke (tasks are interleaved)
- Stack traces might be confusing (jumps around due to scheduling)
- Timing issues might not reproduce (race conditions)

We'll dedicate a whole module to this. For now, just know: **keep async code simple when possible.**

---

## Summary

- **`async def` defines an async function**
- **`await` pauses the function and gives control to the event loop**
- **`asyncio.create_task()` schedules an async function as a task**
- **`asyncio.gather()` waits for multiple tasks**
- **Multiple tasks run concurrently, overlapping their waiting time**
- **Same operations, but concurrency can be 3x-10x faster** depending on workload

## Mental Model Takeaway

Think of `asyncio` as a **task manager**:
- `async def` = register a new task type
- `create_task()` = put a new task on the to-do list
- `await` = "I'm working on this task, but I'm waiting for something. Someone else, handle the next task."
- `gather()` = "Wait until all these tasks are done"
- Event loop = the manager who coordinates which task to work on

## What You Should Now Understand

- How to write basic async code
- How to create and run multiple async tasks
- How concurrency actually works in practice (not theory)
- Why async code can be much faster than sync code
- The difference between `create_task()` + `gather()` (concurrent) vs multiple `await`s (sequential)
- That async is not magic—it's just scheduling

---

Now let's deepen your understanding. Next: understanding `await` deeply and intuitively.
