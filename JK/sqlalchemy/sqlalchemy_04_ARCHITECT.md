# SQLAlchemy 04: ARCHITECT

**Target Audience**: Staff Engineer / System Architect.  
**Philosophy**: Focus on "Design choices, Trade-offs, and Systems Theory".  
**Content Scope**: Internals Deep Dive, Compiler/Interpreter Theory, Scalability, Language Design.

## Internals Deep Dive: SQLAlchemy Core Architecture

### Expression Language and Compilation
SQLAlchemy's core: building SQL from Python expressions:

```python
# Architectural view of SQL compilation
from sqlalchemy import select, column, table

# Define table structure
users = table('users',
    column('id', Integer),
    column('name', String),
    column('email', String)
)

# Build query expression
query = select(users.c.name, users.c.email).where(users.c.id == 1)

# Compilation process
from sqlalchemy.sql.compiler import SQLCompiler

compiler = SQLCompiler(engine.dialect, None)
sql, params = compiler.process(query)

print(sql)  # "SELECT users.name, users.email FROM users WHERE users.id = ?"
print(params)  # [1]
```

### ORM Layer Architecture
The ORM builds on Core with identity mapping and unit of work:

```python
# Simplified Unit of Work implementation
class UnitOfWork:
    def __init__(self):
        self.new_objects = set()      # Objects to INSERT
        self.dirty_objects = set()    # Objects to UPDATE
        self.deleted_objects = set()  # Objects to DELETE
        self.identity_map = {}        # Cache loaded objects
    
    def register_new(self, obj):
        self.new_objects.add(obj)
    
    def register_dirty(self, obj):
        self.dirty_objects.add(obj)
    
    def register_deleted(self, obj):
        self.deleted_objects.add(obj)
    
    def commit(self):
        # Generate SQL for all changes
        self._insert_new()
        self._update_dirty()
        self._delete_removed()
```

## Memory Layout and Object Identity

### Identity Map Implementation
SQLAlchemy's identity map prevents duplicate objects:

```python
class IdentityMap:
    def __init__(self):
        self._cache = {}  # (class, primary_key) -> object
    
    def get(self, class_, primary_key):
        return self._cache.get((class_, primary_key))
    
    def put(self, obj):
        key = (obj.__class__, obj.id)
        self._cache[key] = obj
    
    def clear(self):
        self._cache.clear()

# Usage in session
class Session:
    def __init__(self):
        self.identity_map = IdentityMap()
        self.uow = UnitOfWork()
    
    def query(self, class_):
        # Check identity map first
        # Then query database
        # Store results in identity map
        pass
```

## Scalability: Distributed System Implications

### Connection Pooling Strategies
Architectural decisions for high-traffic systems:

```python
from sqlalchemy import create_engine, pool
from sqlalchemy.ext.asyncio import create_async_engine

# Synchronous pooling for web apps
sync_engine = create_engine(
    'postgresql://...',
    poolclass=pool.QueuePool,
    pool_size=20,          # Base connections
    max_overflow=30,       # Burst capacity
    pool_timeout=60,       # Wait time
    pool_recycle=3600,     # Connection lifetime
    pool_pre_ping=True     # Health checks
)

# Async pooling for high concurrency
async_engine = create_async_engine(
    'postgresql+asyncpg://...',
    pool_size=50,
    max_overflow=100,
    # Async-specific optimizations
)
```

### Sharding and Data Partitioning
Architecting for horizontal scalability:

```python
class ShardEngine:
    def __init__(self, shard_configs):
        self.shards = [create_engine(config) for config in shard_configs]
    
    def get_shard(self, user_id):
        """Route to appropriate shard based on user_id"""
        shard_index = hash(user_id) % len(self.shards)
        return self.shards[shard_index]
    
    def execute_on_shard(self, query, user_id):
        shard_engine = self.get_shard(user_id)
        with shard_engine.connect() as conn:
            return conn.execute(query)

# Usage
shard_engine = ShardEngine([
    'postgresql://shard1...',
    'postgresql://shard2...',
    'postgresql://shard3...'
])

# Queries automatically route to correct shard
results = shard_engine.execute_on_shard(
    "SELECT * FROM users WHERE id = %s", user_id
)
```

## Compiler/Interpreter Theory: Query Compilation

### AST Generation and Optimization
SQLAlchemy builds abstract syntax trees for queries:

```python
# Conceptual AST representation
class Select:
    def __init__(self, columns, from_clause, where_clause=None):
        self.columns = columns
        self.from_clause = from_clause
        self.where_clause = where_clause
    
    def compile(self, dialect):
        # Generate SQL for specific database
        sql_parts = []
        sql_parts.append("SELECT")
        sql_parts.append(", ".join(col.compile(dialect) for col in self.columns))
        sql_parts.append("FROM")
        sql_parts.append(self.from_clause.compile(dialect))
        
        if self.where_clause:
            sql_parts.append("WHERE")
            sql_parts.append(self.where_clause.compile(dialect))
        
        return " ".join(sql_parts)

# Dialect-specific compilation
class PostgreSQLCompiler:
    def visit_column(self, column):
        # PostgreSQL-specific quoting
        return f'"{column.name}"'
    
    def visit_string_literal(self, literal):
        # PostgreSQL-specific escaping
        return f"'{literal.value.replace(chr(39), chr(39)*2)}'"

class MySQLCompiler:
    def visit_column(self, column):
        # MySQL backtick quoting
        return f'`{column.name}`'
```

### Query Planning and Optimization
SQLAlchemy's approach to query optimization:

```python
class QueryOptimizer:
    def optimize(self, query):
        """Apply optimization rules"""
        # Rule 1: Push down selections
        query = self._push_selections(query)
        
        # Rule 2: Eliminate redundant joins
        query = self._eliminate_redundant_joins(query)
        
        # Rule 3: Use indexes where available
        query = self._optimize_index_usage(query)
        
        return query
    
    def _push_selections(self, query):
        """Move WHERE clauses closer to data sources"""
        # Implementation would analyze query structure
        # and reorder operations for efficiency
        pass
```

## Language Design: Why SQLAlchemy Exists

### Impedance Mismatch Problem
Bridging object-oriented and relational paradigms:

```python
# The impedance mismatch
# Relational world: Tables with foreign keys
CREATE TABLE users (id INTEGER, name TEXT);
CREATE TABLE posts (id INTEGER, user_id INTEGER REFERENCES users(id));

# Object world: Objects with references
class User:
    def __init__(self, name):
        self.name = name
        self.posts = []  # List of Post objects

class Post:
    def __init__(self, content, user):
        self.content = content
        self.user = user  # Reference to User object

# SQLAlchemy bridges this gap
user = User(name="Alice")
post = Post(content="Hello!", user=user)
session.add(user)
session.add(post)
session.commit()  # Handles foreign key relationships automatically
```

### Design Philosophy: Explicit over Implicit
SQLAlchemy chooses explicit control over magic:

```python
# Explicit approach (SQLAlchemy)
from sqlalchemy import select

# Build query step by step
query = select(User).where(User.age > 21).order_by(User.name)
results = session.execute(query).scalars().all()

# vs Implicit approach (some ORMs)
# results = User.objects.filter(age__gt=21).order_by('name')
# (Magic method resolution and string parsing)
```

## Trade-offs in Design Choices

### Performance vs Developer Experience
- **Raw SQL Access**: `session.execute(text("SELECT * FROM users"))` for performance
- **ORM Overhead**: Object mapping adds CPU/memory cost for convenience
- **Lazy Loading**: Load data on-demand vs eager loading everything

### Flexibility vs Safety
- **Dynamic Queries**: `session.query(User).filter_by(**filters)` vs static type safety
- **Raw SQL**: Full database power vs ORM protections
- **Schema Reflection**: Auto-discover tables vs explicit model definitions

### Memory vs Speed
- **Identity Map**: Prevents duplicates but uses memory
- **Query Caching**: Faster repeated queries but memory overhead
- **Connection Pooling**: Ready connections vs startup time

## Summary
SQLAlchemy's architecture balances the complexity of object-relational mapping with performance and developer experience. Design choices prioritize explicit control, flexibility, and database portability over magical abstractions.