# Question 5: Get running total of sales by date

## Explanation

A running total (or cumulative sum) calculates the sum of a column's values incrementally, row by row. In SQL, we can achieve this using the `SUM()` window function with the `OVER` clause.

### Key Points:
- `SUM()`: Calculates the sum of a column.
- `OVER (ORDER BY column)`: Defines the order in which rows are processed for the running total.

### SQL Schema
Assume we have a table `Sales` with the following schema:
```sql
CREATE TABLE Sales (
    id INT PRIMARY KEY,
    sale_date DATE,
    amount INT
);
```

### Example Data
```sql
INSERT INTO Sales (id, sale_date, amount) VALUES
(1, '2026-01-01', 100),
(2, '2026-01-02', 200),
(3, '2026-01-03', 300),
(4, '2026-01-04', 400);
```

### Query to Get Running Total
```sql
SELECT sale_date, amount,
       SUM(amount) OVER (ORDER BY sale_date) AS running_total
FROM Sales;
```

### Explanation of the Query
1. `SUM(amount)`: Calculates the sum of the `amount` column.
2. `OVER (ORDER BY sale_date)`: Defines the order of rows by `sale_date` for the running total.

### Output
For the example data, the output will be:
```
sale_date  | amount | running_total
-----------------------------------
2026-01-01 | 100    | 100
2026-01-02 | 200    | 300
2026-01-03 | 300    | 600
2026-01-04 | 400    | 1000
```

---

## Testable Code Module

### Python Script to Test the Query
Below is a Python script using SQLite to test the query:

```python
import sqlite3

def get_running_total():
    # Connect to SQLite database (or create in-memory database)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Create Sales table
    cursor.execute('''
    CREATE TABLE Sales (
        id INTEGER PRIMARY KEY,
        sale_date DATE,
        amount INTEGER
    );
    ''')

    # Insert example data
    sales = [
        (1, '2026-01-01', 100),
        (2, '2026-01-02', 200),
        (3, '2026-01-03', 300),
        (4, '2026-01-04', 400)
    ]
    cursor.executemany('INSERT INTO Sales VALUES (?, ?, ?)', sales)

    # Query to get running total
    running_total_query = '''
    SELECT sale_date, amount,
           SUM(amount) OVER (ORDER BY sale_date) AS running_total
    FROM Sales;
    '''

    cursor.execute(running_total_query)
    print("Running Total Results:")
    for row in cursor.fetchall():
        print(row)

    # Close the connection
    conn.close()

if __name__ == '__main__':
    get_running_total()
```

### How to Run
1. Copy the script into a Python file (e.g., `get_running_total.py`).
2. Run the script using Python.
3. Verify the output matches the expected results.

---

Happy Learning 🚀