# 8. Run Multiple Async Tasks Together

Running multiple async tasks together is one of the most powerful features of async programming. It allows you to handle many tasks efficiently without waiting for each one to finish before starting the next.

---

## The Problem

Imagine you’re downloading three files:
1. `file1.txt` takes 2 seconds.
2. `file2.txt` takes 3 seconds.
3. `file3.txt` takes 1 second.

If you download them one by one, the total time is 2 + 3 + 1 = 6 seconds. But if you download them concurrently, the total time is just the longest download time: 3 seconds.

---

## Using `asyncio.gather()`

The `asyncio.gather()` function allows you to run multiple tasks concurrently. Here’s an example:

```python
import asyncio

async def download_file(file_name, delay):
    print(f"Starting download: {file_name}")
    await asyncio.sleep(delay)  # Simulate download time
    print(f"Download complete: {file_name}")

async def main():
    await asyncio.gather(
        download_file("file1.txt", 2),
        download_file("file2.txt", 3),
        download_file("file3.txt", 1)
    )

asyncio.run(main())
```

### Output:
```
Starting download: file1.txt
Starting download: file2.txt
Starting download: file3.txt
Download complete: file3.txt
Download complete: file1.txt
Download complete: file2.txt
```

---

## Using `asyncio.create_task()`

Another way to run multiple tasks is by using `asyncio.create_task()`. This function schedules a task to run in the background.

```python
async def main():
    task1 = asyncio.create_task(download_file("file1.txt", 2))
    task2 = asyncio.create_task(download_file("file2.txt", 3))
    task3 = asyncio.create_task(download_file("file3.txt", 1))

    await task1
    await task2
    await task3

asyncio.run(main())
```

### Key Difference
- `asyncio.gather()`: Waits for all tasks to complete.
- `asyncio.create_task()`: Schedules tasks to run, and you can `await` them individually.

---

## When to Use Each
- Use `asyncio.gather()` when you want to wait for all tasks to complete together.
- Use `asyncio.create_task()` when you need more control over individual tasks.

---

## Summary
- You can run multiple async tasks together using `asyncio.gather()` or `asyncio.create_task()`.
- `asyncio.gather()` is simpler and waits for all tasks to complete.
- `asyncio.create_task()` gives you more control over individual tasks.

### Mental Model Takeaway
Think of `asyncio.gather()` as a group project where everyone finishes together, and `asyncio.create_task()` as assigning tasks to individuals and checking on them later.

### Intuition You Should Now Have
You should now understand how to run multiple async tasks concurrently and when to use `asyncio.gather()` vs `asyncio.create_task()`.