# 3. Concurrency vs Parallelism

## The Difference Between Concurrency and Parallelism

Concurrency and parallelism are two concepts that are often confused, but they are fundamentally different. Let’s break them down:

- **Concurrency**: Doing multiple tasks by switching between them. Think of it as multitasking.
- **Parallelism**: Doing multiple tasks at the exact same time. Think of it as having multiple workers.

### Real-Life Analogy: The Chef and the Kitchen
Imagine a chef in a kitchen:
- **Concurrency**: The chef is cooking multiple dishes by switching between them. They chop vegetables for one dish, then stir a pot for another, then check the oven for a third. The chef is doing one thing at a time but juggling multiple tasks.
- **Parallelism**: There are multiple chefs in the kitchen, each working on a different dish at the same time. One chef chops vegetables while another stirs the pot and a third checks the oven. Multiple tasks are happening simultaneously.

---

## Why This Matters in Computing

### Concurrency
Concurrency is about structure. It allows a program to handle multiple tasks by switching between them. For example:
- A web server can handle multiple users by switching between their requests.
- A video player can download the next part of a video while playing the current part.

### Parallelism
Parallelism is about execution. It allows a program to perform multiple tasks at the same time. For example:
- A computer with multiple CPUs can process different tasks on each CPU simultaneously.
- A graphics card can render different parts of an image at the same time.

### Key Insight
Concurrency does not require multiple CPUs. It’s about managing tasks efficiently. Parallelism, on the other hand, requires hardware that can execute multiple tasks simultaneously.

---

## Visual Imagination: The Theater
Imagine a theater:
- **Concurrency**: There’s one stage, and the crew switches between different scenes. They set up one scene, perform it, then switch to the next. Only one scene is performed at a time, but the crew is juggling multiple scenes.
- **Parallelism**: There are multiple stages, and different scenes are performed on each stage at the same time. The audience can watch multiple performances simultaneously.

---

## Summary
- **Concurrency** is about juggling multiple tasks by switching between them.
- **Parallelism** is about performing multiple tasks at the same time.
- Concurrency is like a single chef multitasking; parallelism is like multiple chefs working simultaneously.

### Mental Model Takeaway
Think of concurrency as a single worker juggling tasks and parallelism as multiple workers dividing the tasks.

### Intuition You Should Now Have
You should now understand the difference between concurrency and parallelism, and why concurrency is about managing tasks while parallelism is about executing them simultaneously.