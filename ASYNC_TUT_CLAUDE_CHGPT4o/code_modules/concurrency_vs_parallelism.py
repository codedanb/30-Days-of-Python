"""
Module: Concurrency vs Parallelism

This module demonstrates the difference between concurrency and parallelism using simple examples.
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor

def concurrency_example():
    """Simulate concurrency by switching between tasks."""
    print("Starting concurrency example...")
    for i in range(3):
        print(f"Task {i+1}: Working...")
    print("Concurrency example complete!")

def parallelism_example():
    """Simulate parallelism using threads."""
    def task(name):
        print(f"Task {name}: Starting...")
        time.sleep(2)
        print(f"Task {name}: Complete!")

    with ThreadPoolExecutor() as executor:
        executor.submit(task, "A")
        executor.submit(task, "B")

async def async_concurrency_example():
    """Simulate concurrency using async tasks."""
    async def task(name):
        print(f"Task {name}: Starting...")
        await asyncio.sleep(2)
        print(f"Task {name}: Complete!")

    await asyncio.gather(task("A"), task("B"))

# Testable functions
def test_concurrency():
    print("--- Concurrency Example ---")
    concurrency_example()

def test_parallelism():
    print("--- Parallelism Example ---")
    parallelism_example()

def test_async_concurrency():
    print("--- Async Concurrency Example ---")
    asyncio.run(async_concurrency_example())

if __name__ == "__main__":
    test_concurrency()
    test_parallelism()
    test_async_concurrency()