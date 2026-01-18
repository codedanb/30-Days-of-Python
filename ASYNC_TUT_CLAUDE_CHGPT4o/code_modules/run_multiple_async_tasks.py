"""
Module: Run Multiple Async Tasks Together

This module demonstrates how to run multiple async tasks concurrently.
"""
import asyncio

async def download_file(file_name, delay):
    """Simulate downloading a file."""
    print(f"Starting download: {file_name}")
    await asyncio.sleep(delay)
    print(f"Download complete: {file_name}")

async def main():
    """Run multiple tasks concurrently."""
    await asyncio.gather(
        download_file("file1.txt", 2),
        download_file("file2.txt", 3),
        download_file("file3.txt", 1)
    )

# Testable function
def test_run_multiple_tasks():
    print("--- Run Multiple Async Tasks ---")
    asyncio.run(main())

if __name__ == "__main__":
    test_run_multiple_tasks()