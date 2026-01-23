# Pydantic 03: ADVANCED

**Target Audience**: Senior Platform Engineer / Tech Lead.  
**Philosophy**: Focus on "Optimization, Best Practices, and Internals".  
**Content Scope**: Concurrency, Metaprogramming, Design Patterns, Tooling & Linting, Memory profiling.

## Advanced Field Types and Constraints
Beyond basic types, use advanced validation:

```python
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Union
from datetime import datetime
from uuid import UUID
import re

class AdvancedUser(BaseModel):
    id: UUID
    email: str = Field(regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    created_at: datetime
    metadata: Dict[str, Union[str, int]] = {}
    tags: List[str] = Field(max_items=10, unique_items=True)
    
    @validator('email')
    def email_must_be_valid(cls, v):
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', v):
            raise ValueError('Invalid email format')
        return v.lower()
```

## Custom Field Types with Constrained Types
Create reusable constrained types:

```python
from pydantic import BaseModel, conint, constr, conlist

PositiveInt = conint(gt=0)
Username = constr(min_length=3, max_length=50, regex=r'^[a-zA-Z0-9_]+$')
TagList = conlist(str, max_items=5, unique_items=True)

class User(BaseModel):
    user_id: PositiveInt
    username: Username
    tags: TagList = []
```

## Metaprogramming with __init_subclass__
Create model factories and inheritance patterns:

```python
from pydantic import BaseModel
from typing import Any, Dict

class TimestampedModel(BaseModel):
    created_at: float
    updated_at: float
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Add automatic timestamping
        original_init = cls.__init__
        
        def new_init(self, *args, **kwargs):
            import time
            now = time.time()
            if 'created_at' not in kwargs:
                kwargs['created_at'] = now
            kwargs['updated_at'] = now
            original_init(self, *args, **kwargs)
        
        cls.__init__ = new_init

class User(TimestampedModel):
    name: str
    email: str

# Automatic timestamps
user = User(name="Alice", email="alice@example.com")
print(user.created_at)  # Current timestamp
```

## Context Managers and Resource Management
Use Pydantic with context managers for resource handling:

```python
from pydantic import BaseModel
from contextlib import contextmanager
from typing import Generator

class DatabaseConfig(BaseModel):
    host: str
    port: int
    database: str
    user: str
    password: str
    
    @contextmanager
    def connection(self) -> Generator[Any, None, None]:
        # Simulate database connection
        conn = f"Connected to {self.database}"
        try:
            yield conn
        finally:
            print("Connection closed")

config = DatabaseConfig(
    host="localhost", port=5432, database="mydb", 
    user="admin", password="secret"
)

with config.connection() as conn:
    print(conn)  # "Connected to mydb"
# "Connection closed"
```

## Performance Optimization
Use `validate_assignment` and `validate_all` judiciously:

```python
from pydantic import BaseModel

class OptimizedModel(BaseModel):
    name: str
    value: int
    
    class Config:
        validate_assignment = True  # Validate on attribute assignment
        validate_all = False  # Don't validate all fields if one fails

# Fast creation
model = OptimizedModel(name="test", value=42)
model.value = 100  # Automatically validated
```

## Design Patterns: Factory Pattern
Create model factories for different use cases:

```python
from pydantic import BaseModel
from typing import Type, TypeVar
from abc import ABC, abstractmethod

T = TypeVar('T', bound='BaseEntity')

class BaseEntity(BaseModel, ABC):
    id: int
    
    @classmethod
    def create(cls: Type[T], **data) -> T:
        # Factory method
        return cls(id=generate_id(), **data)

class User(BaseEntity):
    name: str
    email: str

class Product(BaseEntity):
    name: str
    price: float

# Usage
user = User.create(name="Alice", email="alice@example.com")
product = Product.create(name="Widget", price=19.99)
```

## Tooling and Linting
Configure Pydantic with mypy and other tools:

```python
# mypy.ini
[mypy]
plugins = pydantic.mypy
follow_imports = silent
warn_redundant_casts = True
warn_unused_ignores = True
disallow_any_generics = True
check_untyped_defs = True

# In code
from pydantic import BaseModel

class StrictModel(BaseModel):
    class Config:
        arbitrary_types_allowed = False
        extra = 'forbid'  # No extra fields allowed
```

## Memory Profiling
Monitor Pydantic's memory usage:

```python
import tracemalloc
from pydantic import BaseModel
from typing import List

class LargeModel(BaseModel):
    data: List[int]

tracemalloc.start()
model = LargeModel(data=list(range(100000)))
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 1024 / 1024:.2f} MB")
print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")
tracemalloc.stop()
```

## Advanced Validators with pre and each_item
Use validator modes for complex validation:

```python
from pydantic import BaseModel, validator
from typing import List

class BatchProcessor(BaseModel):
    items: List[int]
    
    @validator('items', pre=True, each_item=True)
    def validate_item(cls, v):
        if not isinstance(v, int):
            raise ValueError('Each item must be an integer')
        if v < 0:
            raise ValueError('Items must be non-negative')
        return v * 2  # Transform each item
```

## Summary
Advanced Pydantic usage involves custom types, metaprogramming for dynamic behavior, performance optimization, design patterns for maintainable code, and integration with development tooling for robust applications.