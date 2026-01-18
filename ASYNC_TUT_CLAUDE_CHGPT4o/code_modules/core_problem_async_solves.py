"""
Module: Core Problem Async Solves

This module demonstrates blocking vs non-blocking and why synchronous code fails at scale.
"""
import time
import asyncio

def blocking_example():
    """Simulate a blocking operation."""
    print("Starting blocking task...")
    time.sleep(3)  # Simulate a 3-second blocking task
    print("Blocking task complete!")

async def non_blocking_example():
    """Simulate a non-blocking operation."""
    print("Starting non-blocking task...")
    await asyncio.sleep(3)  # Simulate a 3-second non-blocking task
    print("Non-blocking task complete!")

# Testable functions
def test_blocking():
    print("--- Blocking Example ---")
    blocking_example()

def test_non_blocking():
    print("--- Non-Blocking Example ---")
    asyncio.run(non_blocking_example())

if __name__ == "__main__":
    test_blocking()
    test_non_blocking()