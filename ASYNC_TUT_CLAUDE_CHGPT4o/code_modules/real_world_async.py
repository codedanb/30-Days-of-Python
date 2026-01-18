"""
Module: Real-World Applications of Async

This module demonstrates how async programming enables high-scale APIs and systems like ChatGPT.
"""
import asyncio

async def simulate_high_scale_api():
    """Simulate handling multiple API requests concurrently."""
    async def handle_request(request_id):
        print(f"Handling request {request_id}...")
        await asyncio.sleep(2)  # Simulate processing time
        print(f"Request {request_id} complete!")

    await asyncio.gather(
        *(handle_request(i) for i in range(1, 6))  # Simulate 5 concurrent requests
    )

async def simulate_chatgpt_system():
    """Simulate an async system like ChatGPT handling user queries."""
    async def process_query(user_id, query):
        print(f"User {user_id}: Processing query '{query}'...")
        await asyncio.sleep(3)  # Simulate response generation
        print(f"User {user_id}: Response ready!")

    await asyncio.gather(
        process_query(1, "What is async programming?"),
        process_query(2, "Explain concurrency vs parallelism."),
        process_query(3, "How does ChatGPT work?")
    )

# Testable functions
def test_high_scale_api():
    print("--- High-Scale API Simulation ---")
    asyncio.run(simulate_high_scale_api())

def test_chatgpt_system():
    print("--- ChatGPT System Simulation ---")
    asyncio.run(simulate_chatgpt_system())

if __name__ == "__main__":
    test_high_scale_api()
    test_chatgpt_system()