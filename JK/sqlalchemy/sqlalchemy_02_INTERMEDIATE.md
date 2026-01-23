# SQLAlchemy 02: INTERMEDIATE

**Target Audience**: Junior Developer / Daily User.  
**Philosophy**: Focus on "Getting things done". Standard patterns and libraries.  
**Content Scope**: Standard Library usage, Common Data Structures, Modular programming, Error Handling, File I/O.

## Relationships Between Tables
Real data connects together. Create relationships like family trees:

```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine('sqlite:///school.db')

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    grade_id = Column(Integer, ForeignKey('grades.id'))
    
    # Relationship to access grade
    grade = relationship("Grade", back_populates="students")

class Grade(Base):
    __tablename__ = 'grades'
    
    id = Column(Integer, primary_key=True)
    level = Column(String)  # "1st Grade", "2nd Grade", etc.
    
    # Relationship to access students
    students = relationship("Student", back_populates="grade")

Base.metadata.create_all(engine)
```

## One-to-Many and Many-to-Many Relationships

### One-to-Many (One grade has many students)
```python
Session = sessionmaker(bind=engine)
session = Session()

# Create grades
grade1 = Grade(level="1st Grade")
grade2 = Grade(level="2nd Grade")
session.add_all([grade1, grade2])
session.commit()

# Create students
alice = Student(name="Alice", grade=grade1)
bob = Student(name="Bob", grade=grade1)
charlie = Student(name="Charlie", grade=grade2)

session.add_all([alice, bob, charlie])
session.commit()

# Access relationships
print(f"Students in {grade1.level}:")
for student in grade1.students:
    print(f"  - {student.name}")
```

### Many-to-Many (Students can have multiple teachers, teachers multiple students)
```python
from sqlalchemy import Table

# Association table
student_teacher = Table('student_teacher', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('teacher_id', Integer, ForeignKey('teachers.id'))
)

class Teacher(Base):
    __tablename__ = 'teachers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    # Many-to-many relationship
    students = relationship("Student", 
                          secondary=student_teacher,
                          back_populates="teachers")

# Add to Student class
Student.teachers = relationship("Teacher",
                               secondary=student_teacher,
                               back_populates="students")
```

## Advanced Queries
Filter and sort data like a pro:

```python
# Complex filtering
from sqlalchemy import and_, or_, not_

# Find students in 1st grade with names starting with 'A'
students = session.query(Student).filter(
    and_(
        Student.grade.has(level="1st Grade"),
        Student.name.like('A%')
    )
).all()

# Sorting
students_by_name = session.query(Student).order_by(Student.name).all()

# Limiting results
top_5_students = session.query(Student).limit(5).all()

# Counting
student_count = session.query(Student).count()
```

## Joins and Aggregates
Combine data from multiple tables:

```python
from sqlalchemy import func

# Join tables
results = session.query(Student.name, Grade.level).join(Grade).all()

# Group by and count
grade_counts = session.query(
    Grade.level, 
    func.count(Student.id)
).join(Student).group_by(Grade.level).all()

# Subqueries
subquery = session.query(func.avg(Student.id)).subquery()
above_avg = session.query(Student).filter(Student.id > subquery).all()
```

## Error Handling
Handle database errors gracefully:

```python
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

try:
    # Try to add duplicate primary key
    duplicate_student = Student(id=1, name="Duplicate")
    session.add(duplicate_student)
    session.commit()
except IntegrityError as e:
    print("Database integrity error:", str(e))
    session.rollback()  # Undo the failed transaction
except SQLAlchemyError as e:
    print("Database error:", str(e))
    session.rollback()
finally:
    session.close()
```

## Transactions
Group operations that must succeed or fail together:

```python
try:
    # Start transaction
    session.begin()
    
    # Multiple operations
    new_grade = Grade(level="3rd Grade")
    session.add(new_grade)
    
    new_student = Student(name="David", grade=new_grade)
    session.add(new_student)
    
    session.commit()  # All succeed or all fail
    print("Transaction successful")
except Exception as e:
    session.rollback()
    print("Transaction failed:", str(e))
```

## Modular Programming
Split your database code into separate files:

```python
# models.py
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_engine():
    return create_engine('sqlite:///app.db')

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

# main.py
from models import Base, User
from database import get_session

# Create tables
engine = get_engine()
Base.metadata.create_all(engine)

# Use database
session = get_session()
user = User(name="Alice")
session.add(user)
session.commit()
session.close()
```

## File I/O with Databases
Import/export data from files:

```python
import csv
import json

# Export to CSV
def export_to_csv(filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Grade'])
        
        students = session.query(Student).join(Grade).all()
        for student in students:
            writer.writerow([student.name, student.grade.level])

# Import from JSON
def import_from_json(filename):
    with open(filename, 'r') as jsonfile:
        data = json.load(jsonfile)
        
    for item in data:
        grade = session.query(Grade).filter_by(level=item['grade']).first()
        if not grade:
            grade = Grade(level=item['grade'])
            session.add(grade)
        
        student = Student(name=item['name'], grade=grade)
        session.add(student)
    
    session.commit()

# Usage
export_to_csv('students.csv')
import_from_json('new_students.json')
```

## Common Patterns
- Use relationships to connect tables
- Handle errors with try/except and rollback
- Use transactions for multi-step operations
- Split code into models, database setup, and business logic
- Use joins for complex queries
- Import/export data for backups and migration

## Summary
SQLAlchemy helps you build complex data relationships and handle real-world database operations. Use relationships for connected data, handle errors properly, organize code modularly, and manage transactions for data integrity.