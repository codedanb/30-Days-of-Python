# Question 7: Employees earning more than their manager

## Explanation

To find employees who earn more than their manager, we need to compare the salary of each employee with the salary of their respective manager. This can be achieved by joining the `Employees` table with itself.

### Key Points:
- Use a self-join to compare employees with their managers.
- Filter rows where the employee's salary is greater than the manager's salary.

### SQL Schema
Assume we have a table `Employees` with the following schema:
```sql
CREATE TABLE Employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    salary INT,
    manager_id INT
);
```

### Example Data
```sql
INSERT INTO Employees (id, name, salary, manager_id) VALUES
(1, 'Alice', 10000, NULL),
(2, 'Bob', 8000, 1),
(3, 'Charlie', 12000, 1),
(4, 'David', 7000, 2),
(5, 'Eve', 9000, 2);
```

### Query to Find Employees Earning More Than Their Manager
```sql
SELECT e.name AS employee_name, e.salary AS employee_salary,
       m.name AS manager_name, m.salary AS manager_salary
FROM Employees e
JOIN Employees m
ON e.manager_id = m.id
WHERE e.salary > m.salary;
```

### Explanation of the Query
1. `JOIN Employees m ON e.manager_id = m.id`: Joins the `Employees` table with itself to match employees (`e`) with their managers (`m`).
2. `WHERE e.salary > m.salary`: Filters rows where the employee's salary is greater than the manager's salary.

### Output
For the example data, the output will be:
```
employee_name | employee_salary | manager_name | manager_salary
-------------------------------------------------------------
Charlie       | 12000          | Alice        | 10000
Eve           | 9000           | Bob          | 8000
```

---

## Testable Code Module

### Python Script to Test the Query
Below is a Python script using SQLite to test the query:

```python
import sqlite3

def employees_earning_more_than_manager():
    # Connect to SQLite database (or create in-memory database)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Create Employees table
    cursor.execute('''
    CREATE TABLE Employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        salary INTEGER,
        manager_id INTEGER
    );
    ''')

    # Insert example data
    employees = [
        (1, 'Alice', 10000, None),
        (2, 'Bob', 8000, 1),
        (3, 'Charlie', 12000, 1),
        (4, 'David', 7000, 2),
        (5, 'Eve', 9000, 2)
    ]
    cursor.executemany('INSERT INTO Employees VALUES (?, ?, ?, ?)', employees)

    # Query to find employees earning more than their manager
    query = '''
    SELECT e.name AS employee_name, e.salary AS employee_salary,
           m.name AS manager_name, m.salary AS manager_salary
    FROM Employees e
    JOIN Employees m
    ON e.manager_id = m.id
    WHERE e.salary > m.salary;
    '''

    cursor.execute(query)
    print("Employees Earning More Than Their Manager:")
    for row in cursor.fetchall():
        print(row)

    # Close the connection
    conn.close()

if __name__ == '__main__':
    employees_earning_more_than_manager()
```

### How to Run
1. Copy the script into a Python file (e.g., `employees_more_than_manager.py`).
2. Run the script using Python.
3. Verify the output matches the expected results.

---

Happy Learning 🚀