# Pydantic 01: BASICS

**Target Audience**: Absolute beginner (Grade school student / Non-technical person).  
**Philosophy**: Assume NO prior knowledge. Explain "what" and "why" before "how".  
**Content Scope**: Installation & Setup, Fundamental Syntax & Keywords, Basic Data Types, Simple Logic, Analogy-heavy explanations.

## What is Pydantic?
Imagine you're building a Lego castle. Each Lego brick has a specific shape and color, and you can only connect certain bricks together. Pydantic is like a smart Lego sorter that checks if your bricks (data) fit the right spots before you build. It ensures your data is correct and safe, like a friendly robot that validates your building blocks.

## Why Use Pydantic?
Just like how a recipe needs the right ingredients in the right amounts, computer programs need data in the right format. Pydantic helps prevent mistakes, like putting salt instead of sugar in a cake. It catches errors early, so your program doesn't crash later.

## Installation & Setup
1. Open your computer terminal (like a magic window to talk to your computer).
2. Type: `pip install pydantic` (pip is like a delivery service for code packages).
3. Wait for it to download and install, like waiting for pizza delivery.

## Your First Pydantic Model
A model is like a blueprint for your data. Let's create a simple person blueprint:

```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
```

This is like saying: "A person must have a name (which is text) and an age (which is a number)."

## Basic Data Types
- `str`: Text, like your name "Alice"
- `int`: Whole numbers, like 25
- `float`: Decimal numbers, like 3.14
- `bool`: True or False, like "yes" or "no"

## Simple Validation
Pydantic automatically checks your data:

```python
person = Person(name="Alice", age=25)  # This works!
person = Person(name="Bob", age="thirty")  # This fails - age must be a number!
```

It's like a teacher checking your homework - if it's wrong, it tells you exactly what's wrong.

## Basic Field Validation
You can add simple rules:

```python
from pydantic import BaseModel, Field

class Person(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=150)  # ge = greater or equal, le = less or equal
```

This ensures names aren't empty or too long, and ages are reasonable.

## Error Messages
When validation fails, Pydantic gives helpful messages:

```
ValidationError: 1 validation error for Person
age
  value is not a valid integer (type=type_error.integer)
```

It's like getting a friendly note from your teacher explaining the mistake.

## Basic Logic with Validators
Validators are like custom rules:

```python
from pydantic import BaseModel, validator

class Person(BaseModel):
    name: str
    age: int
    
    @validator('age')
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Age cannot be negative')
        return v
```

This is like adding a special guard that checks if age makes sense.

## Summary
Pydantic is your data guardian. It checks, validates, and protects your program's data from mistakes. Start simple: define models with basic types, add fields with rules, and let Pydantic catch errors for you.