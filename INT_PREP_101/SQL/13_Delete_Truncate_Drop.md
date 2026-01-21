# Question 13: Difference between DELETE, TRUNCATE, DROP

## Explanation

`DELETE`, `TRUNCATE`, and `DROP` are SQL commands used to remove data or tables from a database. Each has distinct use cases and behaviors.

### DELETE
- **Purpose**: Removes specific rows from a table.
- **Syntax**:
  ```sql
  DELETE FROM table_name WHERE condition;
  ```
- **Key Points**:
  - Can use a `WHERE` clause to specify which rows to delete.
  - Logs each deleted row, making it slower for large datasets.
  - Can be rolled back (transaction-safe).

#### Example:
```sql
DELETE FROM Employees WHERE department = 'HR';
```

### TRUNCATE
- **Purpose**: Removes all rows from a table.
- **Syntax**:
  ```sql
  TRUNCATE TABLE table_name;
  ```
- **Key Points**:
  - Cannot use a `WHERE` clause.
  - Faster than `DELETE` because it does not log individual row deletions.
  - Resets auto-increment counters.
  - Cannot be rolled back in some databases.

#### Example:
```sql
TRUNCATE TABLE Employees;
```

### DROP
- **Purpose**: Deletes the entire table (or other database objects).
- **Syntax**:
  ```sql
  DROP TABLE table_name;
  ```
- **Key Points**:
  - Removes the table structure and data permanently.
  - Cannot be rolled back.

#### Example:
```sql
DROP TABLE Employees;
```

### Comparison Table
| Feature               | DELETE                          | TRUNCATE                        | DROP                           |
|-----------------------|---------------------------------|---------------------------------|-------------------------------|
| **Removes Data**      | Specific rows                  | All rows                       | Entire table                  |
| **Removes Structure** | No                             | No                             | Yes                           |
| **WHERE Clause**      | Yes                            | No                             | No                            |
| **Rollback**          | Yes                            | No (in some databases)         | No                            |
| **Performance**       | Slower for large datasets      | Faster                         | Fastest                      |

---

## Testable Code Module

### Python Script to Demonstrate DELETE, TRUNCATE, and DROP
Below is a Python script using SQLite to demonstrate the differences:

```python
import sqlite3

def demonstrate_delete_truncate_drop():
    # Connect to SQLite database (or create in-memory database)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Create Employees table
    cursor.execute('''
    CREATE TABLE Employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT
    );
    ''')

    # Insert example data
    employees = [
        (1, 'Alice', 'HR'),
        (2, 'Bob', 'IT'),
        (3, 'Charlie', 'Finance')
    ]
    cursor.executemany('INSERT INTO Employees VALUES (?, ?, ?)', employees)

    # DELETE example
    print("Before DELETE:")
    cursor.execute("SELECT * FROM Employees;")
    print(cursor.fetchall())

    cursor.execute("DELETE FROM Employees WHERE department = 'HR';")
    print("\nAfter DELETE:")
    cursor.execute("SELECT * FROM Employees;")
    print(cursor.fetchall())

    # TRUNCATE example (simulated in SQLite by deleting all rows)
    cursor.executemany('INSERT INTO Employees VALUES (?, ?, ?)', employees)  # Reinsert data
    print("\nBefore TRUNCATE (Simulated):")
    cursor.execute("SELECT * FROM Employees;")
    print(cursor.fetchall())

    cursor.execute("DELETE FROM Employees;")  # Simulate TRUNCATE
    print("\nAfter TRUNCATE (Simulated):")
    cursor.execute("SELECT * FROM Employees;")
    print(cursor.fetchall())

    # DROP example
    cursor.executemany('INSERT INTO Employees VALUES (?, ?, ?)', employees)  # Reinsert data
    print("\nBefore DROP:")
    cursor.execute("SELECT * FROM Employees;")
    print(cursor.fetchall())

    cursor.execute("DROP TABLE Employees;")
    print("\nAfter DROP:")
    try:
        cursor.execute("SELECT * FROM Employees;")
    except sqlite3.OperationalError as e:
        print("Error:", e)

    # Close the connection
    conn.close()

if __name__ == '__main__':
    demonstrate_delete_truncate_drop()
```

### How to Run
1. Copy the script into a Python file (e.g., `delete_truncate_drop.py`).
2. Run the script using Python.
3. Observe the differences between `DELETE`, `TRUNCATE`, and `DROP`.

---

Happy Learning 🚀