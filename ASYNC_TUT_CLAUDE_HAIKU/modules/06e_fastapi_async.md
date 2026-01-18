# Module 6e: Async in the Real World — FastAPI and Web Servers

## Where Async Shines: Web Applications

Now let's see async in its natural habitat: building web servers. This is where async becomes not just useful, but essential.

## The Problem FastAPI Solves

Before FastAPI, building async web servers was complicated. FastAPI makes it simple and automatic.

Here's what's hard:
- Handling 1,000 concurrent users
- Calling slow databases and APIs
- Doing it efficiently on one server
- Without threading complexity

Here's what's easy with async:
- `async def` your handler
- FastAPI runs it concurrently
- Done

## A Simple FastAPI Server

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}

@app.get("/slow")
async def slow_endpoint():
    await asyncio.sleep(2)
    return {"message": "This took 2 seconds"}

# Run with: uvicorn app:app --reload
```

That's a working async web server. Let's understand what's happening.

## How FastAPI Handles Requests

When a request comes in:

1. **FastAPI receives it**
2. **Creates a task** for your async endpoint function
3. **Schedules it on the event loop**
4. **While that request is waiting** (database query, API call), other requests are being handled
5. **When the wait is done**, the response is sent

This is why async is perfect for web servers.

## The Request Lifecycle: Detailed Walkthrough

Let's trace a single request through FastAPI:

```python
from fastapi import FastAPI
from sqlalchemy import select
import asyncio
import httpx

app = FastAPI()

async def fetch_user_data(user_id: int):
    """Simulate fetching from an API"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}")
        return response.json()

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    # Step 1: Receive request
    print(f"Request for user {user_id}")
    
    # Step 2: Fetch data (slow - API call)
    data = await fetch_user_data(user_id)
    
    # Step 3: Process data (fast - CPU)
    processed = {
        "user_id": user_id,
        "name": data.get("name"),
        "email": data.get("email"),
    }
    
    # Step 4: Send response
    return processed
```

**What happens with 100 concurrent requests:**

**Timeline:**
```
0.0s: Request 1 arrives → start API call, switch to Request 2
0.01s: Request 2 arrives → start API call, switch to Request 3
...
0.99s: Request 100 arrives → start API call
1.0s: Request 1's API returns → process it, send response
1.01s: Request 2's API returns → process it, send response
...
1.0-1.2s: All responses sent

Total: ~1.2 seconds
```

With synchronous code, each request would take ~1 second, so 100 requests = 100 seconds.

With async, 100 requests = 1.2 seconds. **Async made this 80x faster.**

## Concurrent Requests Within a Single Request

Sometimes you need to call multiple APIs for a single request:

```python
@app.get("/user-profile/{user_id}")
async def get_user_profile(user_id: int):
    # Fetch from multiple APIs concurrently
    user_data, posts, comments = await asyncio.gather(
        fetch_user(user_id),
        fetch_posts(user_id),
        fetch_comments(user_id),
    )
    
    return {
        "user": user_data,
        "posts": posts,
        "comments": comments,
    }

async def fetch_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}")
        return response.json()

async def fetch_posts(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}/posts")
        return response.json()

async def fetch_comments(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}/comments")
        return response.json()
```

If each API takes 1 second:
- Sequential: 3 seconds
- Concurrent (async): ~1 second

**This is why async is essential for modern APIs.** APIs call other APIs. Without async, they take N seconds to call N APIs. With async, they take ~1 second.

## Database Operations: Async Drivers

Most databases now have async drivers:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

# Create async engine
engine = create_async_engine("postgresql+asyncpg://user:password@localhost/db")
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@app.get("/users")
async def list_users():
    async with async_session() as session:
        # Async query
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users
```

This is crucial because:
- If you use a synchronous database driver, it blocks the event loop (Bug #4 from Module 6d)
- With async drivers, database calls don't block
- You can handle 1,000 concurrent users without hanging

## Caching: A Common Pattern

```python
from cachetools import TTLCache
import time

# In-memory cache
user_cache = TTLCache(maxsize=1000, ttl=3600)

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    # Check cache
    if user_id in user_cache:
        return user_cache[user_id]
    
    # Fetch from API
    data = await fetch_user_data(user_id)
    
    # Cache it
    user_cache[user_id] = data
    
    return data
```

With async, you can add caching without complexity. It just works.

## Background Tasks

Sometimes you need to do something after sending a response:

```python
from fastapi import BackgroundTasks

@app.post("/users")
async def create_user(user_data: dict, background_tasks: BackgroundTasks):
    # Create user in database
    user = await db.create_user(user_data)
    
    # Send email in background (don't wait for it)
    background_tasks.add_task(send_email, user.email)
    
    # Return immediately
    return {"user_id": user.id}

async def send_email(email: str):
    await asyncio.sleep(1)  # Simulate email sending
    print(f"Email sent to {email}")
```

The user gets a response immediately, while the email is sent in the background.

## Long-Lived Connections: WebSockets

For real-time applications, async shines with WebSockets:

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            
            # Process it
            response = process_message(data)
            
            # Send back
            await websocket.send_text(response)
    except Exception as e:
        await websocket.close()
```

With async, a single process can handle thousands of concurrent WebSocket connections. With synchronous code, you'd need thousands of threads.

## The Trade-Off: Complexity vs Throughput

**With async (FastAPI):**
- Handle 10,000 concurrent users
- Single Python process
- Simple code
- Low resource usage
- Higher throughput

**Without async (Flask):**
- Handle 100 concurrent users per process
- Need 100 processes for 10,000 users
- Simple code initially, but deployment is complex
- High resource usage
- Lower throughput

This is why every modern web framework is adding async support.

## Real-World Example: Building a Simple API

```python
from fastapi import FastAPI, HTTPException
import httpx
import asyncio

app = FastAPI()

# Simulate a database
DATABASE = {
    1: {"id": 1, "name": "Alice"},
    2: {"id": 2, "name": "Bob"},
}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Get a user"""
    if user_id not in DATABASE:
        raise HTTPException(status_code=404, detail="User not found")
    return DATABASE[user_id]

@app.get("/users/{user_id}/github-repos")
async def get_user_github_repos(user_id: int):
    """Get a user's GitHub repos"""
    user = get_user(user_id)  # Not awaited, just returns data
    
    # Call GitHub API
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/users/{user['name']}/repos"
        )
    
    return response.json()

@app.post("/users")
async def create_user(name: str):
    """Create a new user"""
    new_id = max(DATABASE.keys()) + 1
    DATABASE[new_id] = {"id": new_id, "name": name}
    return DATABASE[new_id]

@app.get("/health")
async def health_check():
    """Lightweight health check"""
    return {"status": "healthy"}
```

This simple API can handle thousands of concurrent requests efficiently.

---

## Summary

- **FastAPI makes async web servers simple**
- **Async is essential for handling concurrent users**
- **Without async, you need many processes; with async, one process suffices**
- **Concurrent API calls within a request reduce latency**
- **Database drivers must be async to avoid blocking**
- **Background tasks, caching, WebSockets all work naturally with async**
- **Real-world scale requires async** (ChatGPT, Netflix, Google, etc.)

## Mental Model Takeaway

Think of a FastAPI server as a **restaurant with one chef**:

- **Synchronous (slow)**: Chef takes one order, cooks the whole meal, serves it, then takes the next order
- **Async (fast)**: Chef takes an order, puts it in the oven, takes another order, puts it on the stove, takes another order, chops vegetables. While one dish cooks, the chef is productive on another

Same chef. Same speed of individual operations. But async kitchen handles 10x more orders in the same time.

## What You Should Now Understand

- Why async is essential for modern web servers
- How FastAPI uses async to handle concurrency
- The request lifecycle in an async web application
- How to write concurrent operations within a single request
- Why async drivers (database, HTTP client) matter
- Real-world patterns: caching, background tasks, WebSockets
- That async doesn't just improve performance—it changes what's possible

---

Next: comparing async vs threading, and understanding when to use each. Then: advanced patterns like streaming, cancellation, and building resilient async systems.
