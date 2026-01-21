# Question 1: Write a query to find the 2nd highest salary (no LIMIT)

## Explanation

To find the second highest salary in a table without using `LIMIT`, we can use a subquery. The idea is to find the maximum salary that is less than the highest salary. This can be achieved using the `MAX` function and a subquery.

### Steps:
1. Use a subquery to find the maximum salary.
2. Exclude the highest salary from the main query.
3. Use the `MAX` function again to find the second highest salary.

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

### Query
```sql
SELECT MAX(salary) AS second_highest_salary
FROM Employees
WHERE salary < (SELECT MAX(salary) FROM Employees);
```

### Explanation of the Query
1. The subquery `(SELECT MAX(salary) FROM Employees)` finds the highest salary.
2. The `WHERE salary <` condition excludes the highest salary from the main query.
3. The `MAX(salary)` in the main query finds the second highest salary from the remaining salaries.

### Output
For the example data, the output will be:
```
second_highest_salary
---------------------
6000
```

---

## Testable Code Module

### Python Script to Test the Query
Below is a Python script using SQLite to test the query:

```python
import sqlite3

def find_second_highest_salary():
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

    # Query to find the second highest salary
    query = '''
    SELECT MAX(salary) AS second_highest_salary
    FROM Employees
    WHERE salary < (SELECT MAX(salary) FROM Employees);
    '''

    cursor.execute(query)
    result = cursor.fetchone()
    print("Second Highest Salary:", result[0])

    # Close the connection
    conn.close()

if __name__ == '__main__':
    find_second_highest_salary()
```

### How to Run
1. Copy the script into a Python file (e.g., `second_highest_salary.py`).
2. Run the script using Python.
3. Verify the output matches the expected result.

---

Happy Learning 🚀