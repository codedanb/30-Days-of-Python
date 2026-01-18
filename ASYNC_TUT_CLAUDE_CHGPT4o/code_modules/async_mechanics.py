"""
Module: Async Mechanics

This module explains the event loop, tasks, and cooperative multitasking in async programming.
"""
import asyncio

async def event_loop_example():
    """Demonstrate the event loop managing multiple tasks."""
    async def task(name, delay):
        print(f"Task {name} started.")
        await asyncio.sleep(delay)
        print(f"Task {name} complete.")

    await asyncio.gather(
        task("A", 2),
        task("B", 1),
        task("C", 3)
    )

async def cooperative_multitasking_example():
    """Demonstrate cooperative multitasking."""
    async def task(name):
        for i in range(3):
            print(f"Task {name}: Step {i+1}")
            await asyncio.sleep(1)

    await asyncio.gather(task("A"), task("B"))

# Testable functions
def test_event_loop():
    print("--- Event Loop Example ---")
    asyncio.run(event_loop_example())

def test_cooperative_multitasking():
    print("--- Cooperative Multitasking Example ---")
    asyncio.run(cooperative_multitasking_example())

if __name__ == "__main__":
    test_event_loop()
    test_cooperative_multitasking()