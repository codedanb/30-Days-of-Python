# 10. Apply Async Concepts to FastAPI

FastAPI is a modern web framework for building APIs with Python. It’s designed to take full advantage of async programming, making it an excellent choice for high-performance web applications.

---

## Why Use Async in FastAPI?

FastAPI is built on top of Starlette and Pydantic, and it natively supports async programming. Here’s why async is useful in FastAPI:
- **Handle Many Requests:** Async allows the server to handle multiple requests concurrently.
- **Non-Blocking I/O:** Async is perfect for tasks like database queries, API calls, and file operations.
- **High Performance:** FastAPI is one of the fastest Python frameworks, thanks to its async capabilities.

---

## Step 1: Install FastAPI and Uvicorn

To get started, install FastAPI and Uvicorn (an ASGI server):

```bash
pip install fastapi uvicorn
```

---

## Step 2: Create a Simple Async API

Here’s an example of an async FastAPI application:

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/slow-task")
async def slow_task():
    await asyncio.sleep(5)  # Simulate a slow operation
    return {"message": "Task complete!"}

@app.get("/fast-task")
async def fast_task():
    return {"message": "This was quick!"}
```

### Explanation:
- `@app.get("/slow-task")`: Defines an endpoint that simulates a slow operation using `await asyncio.sleep(5)`.
- `@app.get("/fast-task")`: Defines a quick endpoint that doesn’t use `await`.

---

## Step 3: Run the Server

Run the server using Uvicorn:

```bash
uvicorn main:app --reload
```

- `main`: The name of the Python file (without `.py`).
- `app`: The FastAPI instance.
- `--reload`: Enables auto-reloading for development.

Visit the endpoints in your browser:
- [http://127.0.0.1:8000/slow-task](http://127.0.0.1:8000/slow-task)
- [http://127.0.0.1:8000/fast-task](http://127.0.0.1:8000/fast-task)

---

## Step 4: Add Concurrent Tasks

Let’s modify the API to handle multiple tasks concurrently:

```python
@app.get("/multiple-tasks")
async def multiple_tasks():
    task1 = asyncio.create_task(asyncio.sleep(3))
    task2 = asyncio.create_task(asyncio.sleep(2))
    task3 = asyncio.create_task(asyncio.sleep(1))

    await task1
    await task2
    await task3

    return {"message": "All tasks complete!"}
```

### Explanation:
- `asyncio.create_task()`: Schedules tasks to run concurrently.
- `await task1`: Waits for the first task to complete.

---

## Step 5: Use Async with Databases

FastAPI works well with async database libraries like `databases` or `SQLAlchemy` (async version). Here’s an example:

### Install Dependencies:
```bash
pip install databases asyncpg
```

### Example Code:
```python
from databases import Database

DATABASE_URL = "postgresql://user:password@localhost/dbname"
database = Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users")
async def get_users():
    query = "SELECT * FROM users"
    return await database.fetch_all(query)
```

### Explanation:
- `database.connect()`: Connects to the database when the app starts.
- `database.fetch_all(query)`: Executes an async query.

---

## Summary
- FastAPI is designed for async programming, making it ideal for high-performance APIs.
- Use `async def` for endpoints to take advantage of async features.
- Combine FastAPI with async libraries for tasks like database queries.

### Mental Model Takeaway
Think of FastAPI as a high-speed train that uses async to handle multiple passengers (requests) efficiently.

### Intuition You Should Now Have
You should now understand how to use async in FastAPI to build efficient, high-performance APIs.