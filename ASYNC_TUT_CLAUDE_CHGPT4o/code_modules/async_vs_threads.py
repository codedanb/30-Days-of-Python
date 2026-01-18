"""
Module: Async vs Threads

This module compares async programming with threads.
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor

def thread_example():
    """Demonstrate threading for parallelism."""
    import time

    def task(name):
        print(f"Task {name} starting...")
        time.sleep(2)
        print(f"Task {name} complete!")

    with ThreadPoolExecutor() as executor:
        executor.submit(task, "A")
        executor.submit(task, "B")

async def async_example():
    """Demonstrate async for concurrency."""
    async def task(name):
        print(f"Task {name} starting...")
        await asyncio.sleep(2)
        print(f"Task {name} complete!")

    await asyncio.gather(task("A"), task("B"))

# Testable functions
def test_thread_example():
    print("--- Thread Example ---")
    thread_example()

def test_async_example():
    print("--- Async Example ---")
    asyncio.run(async_example())

if __name__ == "__main__":
    test_thread_example()
    test_async_example()