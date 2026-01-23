# SQLAlchemy 03: ADVANCED

**Target Audience**: Senior Platform Engineer / Tech Lead.  
**Philosophy**: Focus on "Optimization, Best Practices, and Internals".  
**Content Scope**: Concurrency, Metaprogramming, Design Patterns, Tooling & Linting, Memory profiling.

## Connection Pooling and Engine Configuration
Optimize database connections for performance:

```python
from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker, scoped_session

# Advanced engine configuration
engine = create_engine(
    'postgresql://user:pass@localhost/db',
    poolclass=pool.QueuePool,  # Connection pooling
    pool_size=10,               # Keep 10 connections ready
    max_overflow=20,            # Allow up to 20 extra connections
    pool_timeout=30,            # Wait 30s for connection
    pool_recycle=3600,          # Recycle connections every hour
    echo=True                   # Log SQL statements (dev only)
)

# Thread-safe session management
Session = scoped_session(sessionmaker(bind=engine))
```

## Concurrency with Async SQLAlchemy
Handle multiple database operations simultaneously:

```python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Async engine
async_engine = create_async_engine('postgresql+asyncpg://user:pass@localhost/db')

# Async session
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def async_database_operations():
    async with AsyncSessionLocal() as session:
        # Multiple async operations
        tasks = [
            session.execute("SELECT * FROM users WHERE id = :id", {"id": 1}),
            session.execute("SELECT * FROM products WHERE category = :cat", {"cat": "electronics"}),
            session.execute("INSERT INTO logs VALUES (:msg)", {"msg": "Async operation"})
        ]
        
        results = await asyncio.gather(*tasks)
        await session.commit()
        
        return results
```

## Metaprogramming: Dynamic Model Creation
Create models at runtime for flexible schemas:

```python
from sqlalchemy import Column, Integer, String, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base

def create_dynamic_model(table_name, fields):
    """Create a model class dynamically"""
    Base = declarative_base()
    
    # Build columns dynamically
    columns = {'__tablename__': table_name, 'id': Column(Integer, primary_key=True)}
    
    for field_name, field_type in fields.items():
        if field_type == 'string':
            columns[field_name] = Column(String)
        elif field_type == 'integer':
            columns[field_name] = Column(Integer)
    
    # Create the class
    return type(table_name.capitalize(), (Base,), columns)

# Usage
UserModel = create_dynamic_model('users', {
    'name': 'string',
    'age': 'integer',
    'email': 'string'
})

# Use like any other model
user = UserModel(name="Alice", age=30, email="alice@example.com")
```

## Design Patterns: Repository Pattern
Organize data access logic:

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session

class Repository(ABC):
    @abstractmethod
    def get_by_id(self, id: int):
        pass
    
    @abstractmethod
    def get_all(self) -> List:
        pass
    
    @abstractmethod
    def add(self, entity):
        pass
    
    @abstractmethod
    def update(self, entity):
        pass
    
    @abstractmethod
    def delete(self, id: int):
        pass

class UserRepository(Repository):
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, id: int) -> Optional[User]:
        return self.session.query(User).filter(User.id == id).first()
    
    def get_all(self) -> List[User]:
        return self.session.query(User).all()
    
    def add(self, user: User):
        self.session.add(user)
        self.session.commit()
    
    def update(self, user: User):
        self.session.merge(user)
        self.session.commit()
    
    def delete(self, id: int):
        user = self.get_by_id(id)
        if user:
            self.session.delete(user)
            self.session.commit()

# Usage
repo = UserRepository(session)
user = repo.get_by_id(1)
repo.add(User(name="New User"))
```

## Unit of Work Pattern
Manage complex transactions:

```python
class UnitOfWork:
    def __init__(self, session_factory):
        self.session_factory = session_factory
    
    def __enter__(self):
        self.session = self.session_factory()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
    
    def commit(self):
        self.session.commit()
    
    def rollback(self):
        self.session.rollback()

# Usage
with UnitOfWork(sessionmaker(bind=engine)) as uow:
    user = User(name="Alice")
    uow.session.add(user)
    
    product = Product(name="Widget")
    uow.session.add(product)
    
    # Automatic commit on exit, rollback on exception
```

## Query Optimization and Profiling
Analyze and optimize database queries:

```python
from sqlalchemy import text
import time

def profile_query(query, params=None):
    """Profile query execution time and explain plan"""
    start_time = time.time()
    
    if params:
        result = session.execute(query, params)
    else:
        result = session.execute(query)
    
    execution_time = time.time() - start_time
    
    # Get query plan (PostgreSQL)
    explain_query = f"EXPLAIN ANALYZE {query}"
    plan = session.execute(text(explain_query), params or {}).fetchall()
    
    return result.fetchall(), execution_time, plan

# Usage
query = "SELECT * FROM users WHERE age > :age"
results, exec_time, plan = profile_query(query, {"age": 21})
print(f"Query took {exec_time:.3f} seconds")
for line in plan:
    print(line[0])
```

## Memory Profiling
Monitor SQLAlchemy's memory usage:

```python
import tracemalloc
from sqlalchemy.orm import sessionmaker

tracemalloc.start()

# Create many objects
Session = sessionmaker(bind=engine)
session = Session()

users = []
for i in range(10000):
    user = User(name=f"User{i}", email=f"user{i}@example.com")
    users.append(user)

session.add_all(users)
session.commit()

current, peak = tracemalloc.get_traced_memory()
print(f"Current memory: {current / 1024 / 1024:.2f} MB")
print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")

# Check for memory leaks
session.close()
tracemalloc.stop()
```

## Tooling and Linting
Configure development tools for SQLAlchemy:

```python
# alembic/env.py - Database migration configuration
from alembic import context
from sqlalchemy import engine_from_config, pool
from models import Base

config = context.config
target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )
    
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        
        with context.begin_transaction():
            context.run_migrations()

# pytest fixtures for testing
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")

@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def session(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
```

## Advanced Relationships and Loading
Optimize relationship loading strategies:

```python
from sqlalchemy.orm import joinedload, selectinload, subqueryload

# Eager loading strategies
# joinedload - JOIN in single query
users_with_posts = session.query(User).options(
    joinedload(User.posts)
).all()

# selectinload - Separate query for related objects
users_with_posts = session.query(User).options(
    selectinload(User.posts)
).all()

# subqueryload - Subquery for related objects
users_with_posts = session.query(User).options(
    subqueryload(User.posts)
).all()

# Lazy loading (default) - Load when accessed
user = session.query(User).first()
posts = user.posts  # Loads here
```

## Summary
Advanced SQLAlchemy involves connection pooling, async operations, dynamic model creation, design patterns for maintainable code, query profiling, and optimized relationship loading strategies.