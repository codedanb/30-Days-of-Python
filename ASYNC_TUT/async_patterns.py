import asyncio

# Common Async Patterns and Best Practices

async def async_with_timeout():
    """Using asyncio.wait_for for timeouts"""
    try:
        result = await asyncio.wait_for(some_async_operation(), timeout=5.0)
        return result
    except asyncio.TimeoutError:
        print("Operation timed out")
        return None

async def some_async_operation():
    await asyncio.sleep(3)
    return "Done"

async def concurrent_requests():
    """Making multiple concurrent requests"""
    urls = ["url1", "url2", "url3"]
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

async def fetch_url(url):
    # Simulate network request
    await asyncio.sleep(1)
    return f"Data from {url}"

async def producer_consumer():
    """Producer-consumer pattern with asyncio.Queue"""
    queue = asyncio.Queue()

    async def producer():
        for i in range(5):
            await queue.put(f"Item {i}")
            await asyncio.sleep(0.5)

    async def consumer():
        while True:
            item = await queue.get()
            print(f"Consumed: {item}")
            queue.task_done()

    # Start producer and consumer
    await asyncio.gather(producer(), consumer())

async def main():
    print("=== Timeout Example ===")
    await async_with_timeout()

    print("\n=== Concurrent Requests ===")
    results = await concurrent_requests()
    print(results)

    print("\n=== Producer-Consumer (runs for 3 seconds) ===")
    # Run producer-consumer for a limited time
    try:
        await asyncio.wait_for(producer_consumer(), timeout=3.0)
    except asyncio.TimeoutError:
        print("Demo finished")

if __name__ == "__main__":
    asyncio.run(main())