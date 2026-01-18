"""
Module: Async Fundamentals

This module introduces the basics of async programming, including async functions and the `await` keyword.
"""
import asyncio

async def async_function_example():
    """A simple async function."""
    print("Async function started.")
    await asyncio.sleep(2)  # Simulate a delay
    print("Async function complete.")

async def smart_waiting_example():
    """Demonstrate smart waiting with multiple tasks."""
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
def test_async_function():
    print("--- Async Function Example ---")
    asyncio.run(async_function_example())

def test_smart_waiting():
    print("--- Smart Waiting Example ---")
    asyncio.run(smart_waiting_example())

if __name__ == "__main__":
    test_async_function()
    test_smart_waiting()