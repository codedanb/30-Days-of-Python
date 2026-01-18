"""
Module: Common Async Bugs and Failure Modes

This module demonstrates common async bugs and how to avoid them.
"""
import asyncio

def forgetting_await():
    """Example of forgetting `await`."""
    async def say_hello():
        print("Hello!")

    # Missing `await`
    print("This will not execute the async function:", say_hello())

async def blocking_event_loop():
    """Example of blocking the event loop."""
    import time
    print("Blocking the event loop...")
    time.sleep(2)  # This blocks the event loop
    print("This will be delayed!")

async def handle_exceptions():
    """Example of handling exceptions in tasks."""
    async def faulty_task():
        raise ValueError("Something went wrong!")

    task = asyncio.create_task(faulty_task())
    try:
        await task
    except Exception as e:
        print(f"Caught an exception: {e}")

# Testable functions
def test_forgetting_await():
    print("--- Forgetting Await ---")
    forgetting_await()

def test_blocking_event_loop():
    print("--- Blocking Event Loop ---")
    asyncio.run(blocking_event_loop())

def test_handle_exceptions():
    print("--- Handle Exceptions ---")
    asyncio.run(handle_exceptions())

if __name__ == "__main__":
    test_forgetting_await()
    test_blocking_event_loop()
    test_handle_exceptions()