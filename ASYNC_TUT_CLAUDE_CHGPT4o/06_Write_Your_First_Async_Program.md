# 6. Write Your First Async Program

Now that you understand the fundamentals of async programming, let’s write your first async program! We’ll start with a simple example to demonstrate how async works in Python.

---

## Step 1: The Problem

Imagine you want to simulate a scenario where you:
1. Download a file.
2. Process the file.
3. Print a message when the task is complete.

In a synchronous program, these tasks would run one after the other. In an async program, we can run them more efficiently.

---

## Step 2: Writing the Code

Here’s your first async program:

```python
import asyncio

async def download_file():
    print("Starting download...")
    await asyncio.sleep(2)  # Simulate a 2-second download
    print("Download complete!")

async def process_file():
    print("Starting processing...")
    await asyncio.sleep(1)  # Simulate a 1-second processing time
    print("Processing complete!")

async def main():
    print("Starting tasks...")
    await download_file()
    await process_file()
    print("All tasks complete!")

# Run the event loop
asyncio.run(main())
```

---

## Step 3: Explanation

### `async def`
- The `async` keyword is used to define an asynchronous function.
- These functions can use `await` to pause and let other tasks run.

### `await`
- The `await` keyword pauses the function until the awaited task is complete.
- While waiting, the event loop can run other tasks.

### `asyncio.run()`
- This starts the event loop and runs the `main()` function.

---

## Step 4: Running the Program

1. Save the code to a file, e.g., `first_async_program.py`.
2. Run the file in your terminal:
   ```bash
   python first_async_program.py
   ```
3. You should see the following output:
   ```
   Starting tasks...
   Starting download...
   Download complete!
   Starting processing...
   Processing complete!
   All tasks complete!
   ```

---

## Summary
- You wrote your first async program using `async def`, `await`, and `asyncio.run()`.
- Async functions allow the program to pause and resume efficiently.

### Mental Model Takeaway
Think of `await` as a "pause button" that lets the event loop switch to other tasks while waiting.

### Intuition You Should Now Have
You should now understand how to define and run an async program, and how `await` allows tasks to pause and resume.