"""
Module: Understand `await` Deeply

This module demonstrates the use of the `await` keyword in async programming.
"""
import asyncio

async def await_example():
    """Demonstrate the use of `await`."""
    print("Starting task...")
    await asyncio.sleep(2)  # Simulate a delay
    print("Task complete!")

async def multiple_await_example():
    """Run multiple tasks concurrently using `await` and `asyncio.gather`."""
    async def task(name, delay):
        print(f"Task {name} started.")
        await asyncio.sleep(delay)
        print(f"Task {name} complete.")

    await asyncio.gather(
        task("A", 3),
        task("B", 1),
        task("C", 2)
    )

# Testable functions
def test_await_example():
    print("--- Await Example ---")
    asyncio.run(await_example())

def test_multiple_await():
    print("--- Multiple Await Example ---")
    asyncio.run(multiple_await_example())

if __name__ == "__main__":
    test_await_example()
    test_multiple_await()