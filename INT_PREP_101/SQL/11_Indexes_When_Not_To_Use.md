# Question 11: Explain indexes & when NOT to use them

## Explanation

Indexes in SQL are used to speed up the retrieval of data from a database table. They work like a book's index, allowing the database to find rows quickly without scanning the entire table.

### Key Points:
- **Types of Indexes**:
  - **Clustered Index**: Determines the physical order of data in a table. A table can have only one clustered index.
  - **Non-Clustered Index**: Does not affect the physical order of data. A table can have multiple non-clustered indexes.
- **How Indexes Work**: Indexes create a data structure (e.g., B-tree) that allows the database to search efficiently.

### When to Use Indexes
1. **Columns Frequently Queried**: Use indexes on columns that are often used in `WHERE`, `JOIN`, `ORDER BY`, or `GROUP BY` clauses.
2. **Large Tables**: Indexes are more beneficial for large tables.
3. **Unique Constraints**: Use indexes to enforce uniqueness (e.g., primary keys).

### When NOT to Use Indexes
1. **Small Tables**: For small tables, the overhead of maintaining an index may outweigh the performance benefits.
2. **Columns with High Write Operations**: Indexes slow down `INSERT`, `UPDATE`, and `DELETE` operations because the index must also be updated.
3. **Columns with Low Selectivity**: Avoid indexing columns with many duplicate values (e.g., `gender`, `status`), as the index will not significantly improve performance.
4. **Rarely Queried Columns**: If a column is rarely used in queries, indexing it is unnecessary.

### Example
Assume we have a table `Employees`:
```sql
CREATE TABLE Employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(100),
    salary INT
);
```

#### Adding an Index
```sql
CREATE INDEX idx_department ON Employees(department);
```
- **Use Case**: If queries frequently filter by `department`, this index will improve performance.

#### When NOT to Add an Index
- If the `department` column has only a few distinct values (e.g., `HR`, `IT`, `Finance`), the index will not be very effective.

---

## Testable Code Module

### Python Script to Demonstrate Index Usage
Below is a Python script using SQLite to demonstrate when to use and when not to use indexes:

```python
import sqlite3
import time

def demonstrate_indexes():
    # Connect to SQLite database (or create in-memory database)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Create Employees table
    cursor.execute('''
    CREATE TABLE Employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        salary INTEGER
    );
    ''')

    # Insert example data
    departments = ['HR', 'IT', 'Finance']
    employees = [(i, f'Employee {i}', departments[i % 3], 5000 + (i % 5) * 1000) for i in range(1, 100001)]
    cursor.executemany('INSERT INTO Employees VALUES (?, ?, ?, ?)', employees)

    # Query without index
    start_time = time.time()
    cursor.execute("SELECT * FROM Employees WHERE department = 'IT';")
    print("Query without index took:", time.time() - start_time, "seconds")

    # Create index on department
    cursor.execute('CREATE INDEX idx_department ON Employees(department);')

    # Query with index
    start_time = time.time()
    cursor.execute("SELECT * FROM Employees WHERE department = 'IT';")
    print("Query with index took:", time.time() - start_time, "seconds")

    # Drop index
    cursor.execute('DROP INDEX idx_department;')

    # Query after dropping index
    start_time = time.time()
    cursor.execute("SELECT * FROM Employees WHERE department = 'IT';")
    print("Query after dropping index took:", time.time() - start_time, "seconds")

    # Close the connection
    conn.close()

if __name__ == '__main__':
    demonstrate_indexes()
```

### How to Run
1. Copy the script into a Python file (e.g., `demonstrate_indexes.py`).
2. Run the script using Python.
3. Observe the query performance with and without the index.

---

Happy Learning 🚀