import asyncio

async def say_hello():
    print("Hello")
    await asyncio.sleep(1)  # Wait 1 second
    print("World!")

async def main():
    await say_hello()

asyncio.run(main())