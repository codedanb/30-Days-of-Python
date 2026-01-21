# Question 14: Top N records per group

## Explanation

To find the top N records per group in SQL, we can use window functions like `ROW_NUMBER()`, `RANK()`, or `DENSE_RANK()`. These functions allow us to assign a rank to each row within a group, and we can filter the rows based on the rank.

### Key Points:
- **ROW_NUMBER()**: Assigns a unique rank to each row within a group.
- **RANK()**: Assigns the same rank to rows with ties, leaving gaps in the ranking.
- **DENSE_RANK()**: Similar to `RANK()`, but without gaps in the ranking.

### SQL Schema
Assume we have a table `Sales` with the following schema:
```sql
CREATE TABLE Sales (
    id INT PRIMARY KEY,
    product VARCHAR(100),
    category VARCHAR(100),
    amount INT
);
```

### Example Data
```sql
INSERT INTO Sales (id, product, category, amount) VALUES
(1, 'Product A', 'Category 1', 100),
(2, 'Product B', 'Category 1', 200),
(3, 'Product C', 'Category 1', 150),
(4, 'Product D', 'Category 2', 300),
(5, 'Product E', 'Category 2', 250);
```

### Query to Find Top N Records Per Group
#### Using ROW_NUMBER()
```sql
WITH RankedSales AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY category ORDER BY amount DESC) AS rank
    FROM Sales
)
SELECT *
FROM RankedSales
WHERE rank <= 2;
```

### Explanation of the Query
1. `ROW_NUMBER() OVER (PARTITION BY category ORDER BY amount DESC)`: Assigns a rank to each row within each `category`, ordered by `amount` in descending order.
2. `WHERE rank <= 2`: Filters the top 2 records for each category.

### Output
For the example data, the output will be:
```
id | product   | category   | amount | rank
-------------------------------------------
2  | Product B | Category 1 | 200    | 1
3  | Product C | Category 1 | 150    | 2
4  | Product D | Category 2 | 300    | 1
5  | Product E | Category 2 | 250    | 2
```

---

## Testable Code Module

### Python Script to Test the Query
Below is a Python script using SQLite to test the query:

```python
import sqlite3

def top_n_records_per_group():
    # Connect to SQLite database (or create in-memory database)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Create Sales table
    cursor.execute('''
    CREATE TABLE Sales (
        id INTEGER PRIMARY KEY,
        product TEXT,
        category TEXT,
        amount INTEGER
    );
    ''')

    # Insert example data
    sales = [
        (1, 'Product A', 'Category 1', 100),
        (2, 'Product B', 'Category 1', 200),
        (3, 'Product C', 'Category 1', 150),
        (4, 'Product D', 'Category 2', 300),
        (5, 'Product E', 'Category 2', 250)
    ]
    cursor.executemany('INSERT INTO Sales VALUES (?, ?, ?, ?)', sales)

    # Query to find top N records per group
    top_n_query = '''
    WITH RankedSales AS (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY category ORDER BY amount DESC) AS rank
        FROM Sales
    )
    SELECT *
    FROM RankedSales
    WHERE rank <= 2;
    '''

    cursor.execute(top_n_query)
    print("Top N Records Per Group:")
    for row in cursor.fetchall():
        print(row)

    # Close the connection
    conn.close()

if __name__ == '__main__':
    top_n_records_per_group()
```

### How to Run
1. Copy the script into a Python file (e.g., `top_n_records_per_group.py`).
2. Run the script using Python.
3. Verify the output matches the expected results.

---

Happy Learning 🚀