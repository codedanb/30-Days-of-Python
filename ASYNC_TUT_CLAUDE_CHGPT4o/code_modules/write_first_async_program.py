"""
Module: Write Your First Async Program

This module contains the first async program example.
"""
import asyncio

async def download_file():
    """Simulate downloading a file."""
    print("Starting download...")
    await asyncio.sleep(2)  # Simulate a 2-second download
    print("Download complete!")

async def process_file():
    """Simulate processing a file."""
    print("Starting processing...")
    await asyncio.sleep(1)  # Simulate a 1-second processing time
    print("Processing complete!")

async def main():
    """Run the async program."""
    print("Starting tasks...")
    await download_file()
    await process_file()
    print("All tasks complete!")

# Testable function
def test_first_async_program():
    print("--- First Async Program ---")
    asyncio.run(main())

if __name__ == "__main__":
    test_first_async_program()