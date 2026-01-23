# Pydantic 02: INTERMEDIATE

**Target Audience**: Junior Developer / Daily User.  
**Philosophy**: Focus on "Getting things done". Standard patterns and libraries.  
**Content Scope**: Standard Library usage, Common Data Structures, Modular programming, Error Handling, File I/O.

## Nested Models
Real data is often complex, like a Russian doll. Create models inside models:

```python
from pydantic import BaseModel
from typing import List

class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class Person(BaseModel):
    name: str
    age: int
    address: Address
    hobbies: List[str] = []

# Usage
person = Person(
    name="Alice",
    age=30,
    address=Address(street="123 Main St", city="Anytown", zip_code="12345"),
    hobbies=["reading", "coding"]
)
```

## Optional Fields and Defaults
Not all data is required. Use Optional for maybe-data:

```python
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: str
    phone: Optional[str] = None  # Optional field
    is_active: bool = True  # Default value
```

## Custom Validators
Add business logic validation:

```python
from pydantic import BaseModel, validator, ValidationError
from typing import List

class Product(BaseModel):
    name: str
    price: float
    tags: List[str] = []
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v
    
    @validator('tags')
    def tags_must_be_unique(cls, v):
        if len(v) != len(set(v)):
            raise ValueError('Tags must be unique')
        return v
```

## Field Aliases
Sometimes your data comes with different names:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    user_id: int = Field(alias='id')
    full_name: str = Field(alias='name')
    
    class Config:
        allow_population_by_field_name = True

# Both work:
user1 = User(id=1, name="Alice")
user2 = User(user_id=1, full_name="Alice")
```

## Serialization and Deserialization
Convert between Python objects and JSON/dicts:

```python
person = Person(name="Bob", age=25)
person_dict = person.dict()  # To dict
person_json = person.json()  # To JSON string

# From dict/JSON
data = {"name": "Charlie", "age": 35}
person_from_dict = Person(**data)
person_from_json = Person.parse_raw('{"name": "David", "age": 40}')
```

## Error Handling with ValidationError
Catch and handle validation errors gracefully:

```python
from pydantic import ValidationError

try:
    person = Person(name="", age=-5)
except ValidationError as e:
    print("Validation failed:")
    for error in e.errors():
        print(f"Field: {error['loc'][0]}, Error: {error['msg']}")
```

## File I/O with Pydantic
Load and save data using Pydantic models:

```python
import json
from typing import List

class Person(BaseModel):
    name: str
    age: int

def save_people(people: List[Person], filename: str):
    with open(filename, 'w') as f:
        json.dump([p.dict() for p in people], f)

def load_people(filename: str) -> List[Person]:
    with open(filename, 'r') as f:
        data = json.load(f)
    return [Person(**p) for p in data]

# Usage
people = [Person(name="Alice", age=30), Person(name="Bob", age=25)]
save_people(people, 'people.json')
loaded_people = load_people('people.json')
```

## Modular Programming
Split your models into separate files:

```python
# models/person.py
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int

# models/address.py  
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str

# main.py
from models.person import Person
from models.address import Address

person = Person(name="Eve", age=28)
```

## Common Patterns
- Use `BaseModel` for all data structures
- Add validators for business rules
- Use Optional for nullable fields
- Handle ValidationError in try/except blocks
- Use `.dict()` and `.json()` for output
- Use `parse_obj()` or `**data` for input

## Summary
Pydantic helps you build robust data handling in your applications. Use nested models for complex data, add custom validation for business rules, handle errors gracefully, and organize your code modularly.