# Async Programming Learning Checklist

Use this checklist to track your progress through the course.

## Part 1: Foundations

### Module 1: Before Programming
- [ ] Understand what programming is (giving instructions to a dumb machine)
- [ ] Understand how computers execute instructions (one at a time, in order)
- [ ] Understand what "waiting" means in computing (CPU idle time)
- [ ] Understand why blocking is a problem (wasted time, no work gets done)
- [ ] Can explain the librarian analogy

### Module 2: Blocking vs Non-Blocking
- [ ] Understand the core problem async solves (blocking causes CPU idleness)
- [ ] Can explain blocking with a restaurant kitchen analogy
- [ ] Can explain non-blocking with smart chef analogy
- [ ] Understand why blocking fails at scale (100 requests × 1 second = 100 seconds)
- [ ] Understand the solution (smart scheduling of multiple tasks)
- [ ] Can visualize the timeline difference (sync vs async)

### Module 3: Concurrency vs Parallelism
- [ ] Understand concurrency (multiple tasks switching rapidly)
- [ ] Understand parallelism (multiple tasks running simultaneously)
- [ ] Can explain the difference with juggling analogy
- [ ] Understand that async is concurrency, not parallelism
- [ ] Know when concurrency helps (I/O-bound) vs parallelism (CPU-bound)
- [ ] Can answer: "Are async tasks running at the same time?" (No, they switch)

### Module 4: Async Fundamentals
- [ ] Understand what async actually is (concurrency pattern for I/O-bound work)
- [ ] Know what async is NOT (doesn't make things faster, doesn't use multiple cores)
- [ ] Understand the event loop concept (basic idea)
- [ ] Know what async is good for (I/O-bound, many concurrent tasks)
- [ ] Know what async is bad for (CPU-bound work)
- [ ] Understand the paradigm shift (sequential → concurrent thinking)

### Module 5: Async Mechanics
- [ ] Understand how the event loop works (loop + scheduling)
- [ ] Can trace through a multi-task execution timeline
- [ ] Understand what `await` does (creates a pause point)
- [ ] Understand cooperative vs preemptive multitasking
- [ ] Know the difference between single-threaded and parallelism
- [ ] Understand that async doesn't violate single-threaded execution
- [ ] Can explain why `await` is needed

## Part 2: Practical Mastery

### Module 6a: First Async Program
- [ ] Can write a basic async function
- [ ] Can use `asyncio.sleep()`
- [ ] Can create multiple tasks with `create_task()`
- [ ] Can use `asyncio.gather()` to wait for multiple tasks
- [ ] Understand the difference between serial and concurrent (2-task example)
- [ ] Can measure time to see the difference
- [ ] Have run at least 3 examples and seen them work

### Module 6b: Understanding `await`
- [ ] Deeply understand what `await` does (pause + resume)
- [ ] Know `await` can only be used in `async def` functions
- [ ] Understand coroutines (the object returned by `async def`)
- [ ] Know the most common bug: forgetting `await`
- [ ] Can explain why multiple `await`s in a row are sequential
- [ ] Understand the "contagion" of `async def` (spreads up the call chain)
- [ ] Can fix code that has missing `await`

### Module 6c: Running Multiple Tasks
- [ ] Know the `gather()` pattern (run all, wait for all)
- [ ] Know the `wait(FIRST_COMPLETED)` pattern (first result)
- [ ] Know the `as_completed()` pattern (process as they arrive)
- [ ] Know the timeout pattern
- [ ] Know the semaphore pattern (rate limiting)
- [ ] Can choose the right pattern for a given problem
- [ ] Have written 2-3 programs using different patterns

### Module 6d: Common Bugs
- [ ] Know the top 5 async bugs
- [ ] Can identify and fix: forgetting `await`
- [ ] Can identify and fix: creating task but not awaiting
- [ ] Can identify and fix: blocking the event loop
- [ ] Can identify and fix: race conditions
- [ ] Know how to debug async code (print statements, names, debug mode)
- [ ] Have made each mistake and fixed it

### Module 6e: FastAPI and Web Servers
- [ ] Understand how FastAPI uses async automatically
- [ ] Can write a basic FastAPI endpoint
- [ ] Understand the request lifecycle
- [ ] Can call multiple APIs concurrently within one request
- [ ] Know why async is essential for high-scale servers
- [ ] Have built and tested a simple async API
- [ ] Understand caching and background tasks

### Module 6f: Async vs Threads vs Processes
- [ ] Know when to use async (I/O-bound, many concurrent)
- [ ] Know when to use threads (legacy code, lightweight)
- [ ] Know when to use multiprocessing (CPU-bound)
- [ ] Understand the Python GIL and its implications
- [ ] Know the tradeoffs: memory, simplicity, performance
- [ ] Can make a decision: which tool for which problem
- [ ] Have tested at least one comparison

### Module 6g: Advanced Patterns
- [ ] Know the streaming pattern (don't load all into memory)
- [ ] Know the cancellation pattern (graceful shutdown)
- [ ] Know the timeout + retry pattern
- [ ] Know the semaphore pattern (rate limiting)
- [ ] Know the queue pattern (producer-consumer)
- [ ] Know the circuit breaker pattern (prevent cascading failures)
- [ ] Have implemented at least 2 advanced patterns

---

## Skill Level Checklist

### Beginner (After Module 5)
- [ ] Understand why async exists
- [ ] Understand how the event loop works
- [ ] Can read async code and understand what it does
- [ ] Know the basic concepts (await, tasks, event loop)

### Intermediate (After Module 6d)
- [ ] Can write basic async code
- [ ] Can run multiple tasks concurrently
- [ ] Can identify and fix common bugs
- [ ] Can debug async code
- [ ] Can choose between patterns

### Advanced (After Module 6g)
- [ ] Can write production-quality async code
- [ ] Can use advanced patterns (circuit breaker, rate limiting, etc.)
- [ ] Can build real async applications (web servers, APIs)
- [ ] Can optimize async code (connection pooling, caching)
- [ ] Can decide: async vs threading vs multiprocessing for any problem

---

## Hands-On Projects

Track your projects here:

### Project 1: Simple Async Script
- [ ] Write an async function that calls 5 APIs concurrently
- [ ] Measure and show the speedup vs sequential
- **Expected:** 5x faster than sequential

### Project 2: FastAPI Endpoint
- [ ] Create an async endpoint that calls multiple services
- [ ] Show it handles concurrent requests efficiently
- **Expected:** Can handle 100+ concurrent requests

### Project 3: Bug Hunt
- [ ] Take buggy async code and fix all bugs
- [ ] Understand why each bug matters
- **Expected:** All bugs identified and fixed

### Project 4: Pattern Implementation
- [ ] Implement timeout + retry
- [ ] Implement rate limiting with semaphore
- [ ] Implement graceful cancellation
- **Expected:** All patterns working correctly

### Project 5: Real Application
- [ ] Build something real (web scraper, API, real-time app)
- [ ] Use async throughout
- [ ] Handle errors gracefully
- **Expected:** Production-ready async code

### Project 6: Performance Comparison
- [ ] Compare async vs threading vs sync
- [ ] Measure: time, memory, CPU usage
- [ ] Show when each approach is best
- **Expected:** Data-driven understanding

### Project 7: Advanced System
- [ ] Build a system combining multiple patterns
- [ ] Include: concurrency, rate limiting, timeouts, retries
- [ ] Build: robust, scalable, production-ready
- **Expected:** Understanding of real-world async systems

---

## Question Checklist: Can You Answer These?

### Conceptual Questions
- [ ] Why does async exist? (Answer: To handle many I/O-bound tasks efficiently)
- [ ] What problem does async solve? (Answer: CPU idleness while waiting)
- [ ] How is async different from threading? (Answer: Cooperative vs preemptive)
- [ ] Can async make individual requests faster? (Answer: No, but handles more requests)
- [ ] Does async use multiple CPU cores? (Answer: Usually not, that's multiprocessing)
- [ ] What is the event loop? (Answer: A scheduler that runs tasks and pauses at await points)
- [ ] What does `await` do? (Answer: Pauses the function and resumes when ready)
- [ ] Why can't you use `await` in regular functions? (Answer: They can't be paused/resumed)

### Practical Questions
- [ ] How do you run multiple async tasks concurrently? (Answer: `asyncio.gather()` or `create_task()`)
- [ ] What's the most common async bug? (Answer: Forgetting `await`)
- [ ] How do you limit concurrent operations? (Answer: `asyncio.Semaphore()`)
- [ ] How do you add a timeout? (Answer: `asyncio.wait_for()`)
- [ ] How do you retry with backoff? (Answer: Loop with exponential sleep)
- [ ] How do you cancel a task? (Answer: `task.cancel()`)
- [ ] How do you handle exceptions in background tasks? (Answer: `try/except` or callbacks)
- [ ] When should you use async vs threading? (Answer: Async for I/O, threading for legacy)

### Debug Questions
- [ ] You see `<coroutine object>` printed. What went wrong? (Answer: Forgot `await`)
- [ ] A background task runs but you never see the result. Why? (Answer: Didn't await it)
- [ ] The event loop seems frozen. What might be wrong? (Answer: Blocking with `time.sleep()`)
- [ ] Two tasks are accessing the same variable and getting corrupted data. Why? (Answer: Race condition, need lock)
- [ ] Your server is slow. How would you check if it's your async code? (Answer: Profiling, check for sequential awaits)

---

## Learning Pace Guide

### Fast Track (2-3 hours)
- [ ] Read Modules 2-4 (understand problem and solution)
- [ ] Read Module 6a-6c (write code)
- [ ] Run 5 examples

### Standard Track (6-8 hours)
- [ ] Read all Modules 1-7 in order
- [ ] Run examples as you go
- [ ] Do one project from each module

### Deep Dive (2 weeks)
- [ ] Read all modules thoroughly
- [ ] Do all exercises
- [ ] Complete all 7 projects
- [ ] Study production frameworks (FastAPI, aiohttp)
- [ ] Build your own real application

---

## Topic Review Checklist

Return to this section to review core concepts:

### Core Concept 1: The Event Loop
- [ ] Can explain what the event loop is
- [ ] Can trace through a simple multi-task execution
- [ ] Understand it's just a loop managing tasks
- [ ] Not magic, just a scheduling algorithm

### Core Concept 2: `await` and Pause Points
- [ ] Understand `await` creates a pause point
- [ ] Understand the function resumes at the exact `await` line
- [ ] Know `await` can only be used in `async def`
- [ ] Know forgetting `await` is the most common bug

### Core Concept 3: Concurrency, Not Parallelism
- [ ] Understand async is single-threaded (usually)
- [ ] Multiple tasks switch rapidly, not run simultaneously
- [ ] Not designed for CPU-bound work
- [ ] Designed for I/O-bound work (network, disk, database)

### Core Concept 4: Patterns Over Syntax
- [ ] Know the 8 main patterns (gather, first, as_completed, etc.)
- [ ] Can choose the right pattern for a problem
- [ ] Patterns are more important than memorizing syntax
- [ ] Once you know patterns, syntax is easy

### Core Concept 5: Practical Production Code
- [ ] Async code needs error handling
- [ ] Need timeouts to prevent hanging
- [ ] Need retry logic for unreliable services
- [ ] Need rate limiting to not overwhelm services
- [ ] Need monitoring to know what's happening

---

## Red Flags: Common Misunderstandings

If you believe any of these, go back and reread:

- [ ] "Async makes my code faster" → No, it handles more concurrency
- [ ] "Async uses multiple cores" → No, that's multiprocessing
- [ ] "I don't need to understand the event loop" → You do, it's crucial
- [ ] "`await` is a wait command" → No, it's a pause/resume point
- [ ] "Async is always better" → No, it's better for I/O-bound work
- [ ] "I can use async for CPU-intensive work" → No, use multiprocessing
- [ ] "Threading is always worse than async" → No, each has tradeoffs
- [ ] "I'll use async everywhere" → No, use the right tool for each problem

---

## Final Checklist: Ready for Production?

You're ready to use async in production when you can:

- [ ] Write async code that handles errors gracefully
- [ ] Set appropriate timeouts on all external calls
- [ ] Implement retry logic with exponential backoff
- [ ] Rate-limit requests to external services
- [ ] Monitor running tasks and catch hanging tasks
- [ ] Choose between async, threading, and multiprocessing
- [ ] Debug async code when something goes wrong
- [ ] Explain async to colleagues
- [ ] Make decisions about architecture (when to use async)
- [ ] Handle edge cases (cancellation, timeouts, failures)

---

## Resources to Revisit

If you get stuck on a topic, come back here:

- **Concepts unclear?** → Return to the corresponding module
- **Can't write working code?** → Look at examples in `code_examples/all_examples.py`
- **Quick syntax lookup?** → Check `QUICK_REFERENCE.md`
- **Debugging code?** → See Module 6d debugging techniques
- **Architecture decision?** → See Module 6f decision tree

---

## Congratulations!

When you've completed this entire checklist, you've mastered async programming.

You understand not just the syntax, but the concepts. You can write production-ready code. You can debug problems. You can make architecture decisions.

**That's expertise.**

Now go build something amazing with async! 🚀
