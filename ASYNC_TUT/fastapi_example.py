from fastapi import FastAPI
import asyncio

app = FastAPI()

async def slow_operation():
    await asyncio.sleep(2)  # Simulate slow I/O
    return "Done"

@app.get("/async")
async def async_endpoint():
    result = await slow_operation()
    return {"result": result}

@app.get("/sync")
def sync_endpoint():
    import time
    time.sleep(2)  # This blocks!
    return {"result": "Done"}