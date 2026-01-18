import asyncio

async def task1():
    print("Task 1 starting")
    await asyncio.sleep(2)
    print("Task 1 done")

async def task2():
    print("Task 2 starting")
    await asyncio.sleep(1)
    print("Task 2 done")

async def main():
    await asyncio.gather(task1(), task2())
    print("All tasks complete")

asyncio.run(main())