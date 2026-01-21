# Question 4: Rank users by salary using window functions

## Explanation

Window functions in SQL allow us to perform calculations across a set of table rows that are related to the current row. To rank users by salary, we can use the `RANK()` function. This function assigns a rank to each row within a partition of data, with ranks assigned in order of the specified column.

### Key Points:
- `RANK()`: Assigns a unique rank to each row, with gaps in ranking for ties.
- `DENSE_RANK()`: Similar to `RANK()`, but without gaps in ranking for ties.
- `ROW_NUMBER()`: Assigns a unique number to each row, even for ties.

### SQL Schema
Assume we have a table `Employees` with the following schema:
```sql
CREATE TABLE Employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    salary INT
);
```

### Example Data
```sql
INSERT INTO Employees (id, name, salary) VALUES
(1, 'Alice', 5000),
(2, 'Bob', 7000),
(3, 'Charlie', 6000),
(4, 'David', 7000);
```

### Query to Rank Users by Salary
```sql
SELECT name, salary,
       RANK() OVER (ORDER BY salary DESC) AS rank,
       DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank,
       ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_number
FROM Employees;
```

### Explanation of the Query
1. `RANK() OVER (ORDER BY salary DESC)` assigns a rank to each employee based on their salary, with gaps for ties.
2. `DENSE_RANK() OVER (ORDER BY salary DESC)` assigns a rank without gaps for ties.
3. `ROW_NUMBER() OVER (ORDER BY salary DESC)` assigns a unique number to each row, even for ties.

### Output
For the example data, the output will be:
```
name     | salary | rank | dense_rank | row_number
---------------------------------------------------
Bob      | 7000   | 1    | 1          | 1
David    | 7000   | 1    | 1          | 2
Charlie  | 6000   | 3    | 2          | 3
Alice    | 5000   | 4    | 3          | 4
```

---

## Testable Code Module

### Python Script to Test the Query
Below is a Python script using SQLite to test the query:

```python
import sqlite3

def rank_users_by_salary():
    # Connect to SQLite database (or create in-memory database)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Create Employees table
    cursor.execute('''
    CREATE TABLE Employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        salary INTEGER
    );
    ''')

    # Insert example data
    employees = [
        (1, 'Alice', 5000),
        (2, 'Bob', 7000),
        (3, 'Charlie', 6000),
        (4, 'David', 7000)
    ]
    cursor.executemany('INSERT INTO Employees VALUES (?, ?, ?)', employees)

    # Query to rank users by salary
    rank_query = '''
    SELECT name, salary,
           RANK() OVER (ORDER BY salary DESC) AS rank,
           DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank,
           ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_number
    FROM Employees;
    '''

    cursor.execute(rank_query)
    print("Ranking Results:")
    for row in cursor.fetchall():
        print(row)

    # Close the connection
    conn.close()

if __name__ == '__main__':
    rank_users_by_salary()
```

### How to Run
1. Copy the script into a Python file (e.g., `rank_users_by_salary.py`).
2. Run the script using Python.
3. Verify the output matches the expected results.

---

Happy Learning 🚀