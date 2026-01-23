# SQLAlchemy 01: BASICS

**Target Audience**: Absolute beginner (Grade school student / Non-technical person).  
**Philosophy**: Assume NO prior knowledge. Explain "what" and "why" before "how".  
**Content Scope**: Installation & Setup, Fundamental Syntax & Keywords, Basic Data Types, Simple Logic, Analogy-heavy explanations.

## What is SQLAlchemy?
Imagine you have a magical library where books organize themselves. Instead of searching through messy piles, books know exactly where they belong. SQLAlchemy is like that magical librarian for your data. It helps your computer talk to databases (big organized storage boxes) and keeps your data neat and tidy.

## Why Use SQLAlchemy?
Just like how a library helps you find books quickly, SQLAlchemy helps your program find and organize data fast. Without it, you'd have to write complicated database commands. With SQLAlchemy, it's like having a friendly assistant who speaks both computer language and database language.

## Installation & Setup
1. Open your computer terminal.
2. Type: `pip install sqlalchemy` (get the magic librarian software).
3. For this tutorial, we'll use SQLite (a simple database that comes with Python).

## Your First Database Table
A table is like a spreadsheet. Let's create a table for storing information about pets:

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the magic librarian
engine = create_engine('sqlite:///pets.db')

# Create the base for our tables
Base = declarative_base()

# Define a table (like a spreadsheet)
class Pet(Base):
    __tablename__ = 'pets'
    
    id = Column(Integer, primary_key=True)  # Unique number for each pet
    name = Column(String)  # Pet's name
    animal_type = Column(String)  # Dog, cat, etc.

# Create the table in the database
Base.metadata.create_all(engine)
```

## Basic Data Types
- `Integer`: Whole numbers (1, 2, 42)
- `String`: Text ("Fluffy", "Dog")
- `Float`: Decimal numbers (3.14, 10.5)
- `Boolean`: True or False (like yes/no)

## Adding Data to Your Table
Adding data is like writing in your spreadsheet:

```python
# Create a session (like opening your spreadsheet)
Session = sessionmaker(bind=engine)
session = Session()

# Create pet objects
fluffy = Pet(name="Fluffy", animal_type="Cat")
spot = Pet(name="Spot", animal_type="Dog")

# Add them to the database
session.add(fluffy)
session.add(spot)
session.commit()  # Save the changes
```

## Getting Data from Your Table
Reading data is like looking at your spreadsheet:

```python
# Get all pets
all_pets = session.query(Pet).all()
for pet in all_pets:
    print(f"{pet.name} is a {pet.animal_type}")

# Get a specific pet
fluffy = session.query(Pet).filter_by(name="Fluffy").first()
print(f"Found: {fluffy.name}")
```

## Simple Filtering
Find specific data, like searching for books by author:

```python
# Find all cats
cats = session.query(Pet).filter_by(animal_type="Cat").all()

# Find pets with names starting with 'F'
f_pets = session.query(Pet).filter(Pet.name.like('F%')).all()
```

## Updating Data
Change data, like correcting a spelling mistake:

```python
# Find Fluffy
fluffy = session.query(Pet).filter_by(name="Fluffy").first()

# Change her name
fluffy.name = "Fluffykins"
session.commit()
```

## Deleting Data
Remove data, like throwing away an old book:

```python
# Find Spot
spot = session.query(Pet).filter_by(name="Spot").first()

# Remove him
session.delete(spot)
session.commit()
```

## Summary
SQLAlchemy is your data librarian. It helps you:
- Create organized tables for your data
- Add, read, update, and delete information
- Find specific data quickly
- Keep everything neat and organized

Start with simple tables, add some data, and practice finding it back!