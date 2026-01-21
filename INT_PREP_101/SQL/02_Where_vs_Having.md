# Question 2: Difference between WHERE vs HAVING (real example)

## Explanation

Both `WHERE` and `HAVING` are used to filter data in SQL, but they are used in different contexts:

1. **WHERE**: Filters rows before any grouping is performed.
2. **HAVING**: Filters groups after the `GROUP BY` clause is applied.

### Key Differences:
| Feature               | WHERE                          | HAVING                         |
|-----------------------|--------------------------------|--------------------------------|
| Filters on            | Individual rows               | Groups                        |
| Used with Aggregates? | No                            | Yes                           |
| Execution Order       | Before `GROUP BY`             | After `GROUP BY`              |

### Real Example
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
(3, 'Product C', 'Category 2', 300),
(4, 'Product D', 'Category 2', 400);
```

### Query Using WHERE
Find all sales in `Category 1`:
```sql
SELECT *
FROM Sales
WHERE category = 'Category 1';
```

### Query Using HAVING
Find categories with total sales greater than 300:
```sql
SELECT category, SUM(amount) AS total_sales
FROM Sales
GROUP BY category
HAVING SUM(amount) > 300;
```

### Explanation of the Queries
1. The `WHERE` clause filters rows where `category = 'Category 1'` before grouping.
2. The `HAVING` clause filters groups where the total sales (`SUM(amount)`) exceed 300 after grouping.

### Outputs
- **WHERE Query Output**:
```
id | product   | category   | amount
-----------------------------------
1  | Product A | Category 1 | 100
2  | Product B | Category 1 | 200
```

- **HAVING Query Output**:
```
category   | total_sales
------------------------
Category 2 | 700
```

---

## Testable Code Module

### Python Script to Test the Queries
Below is a Python script using SQLite to test the queries:

```python
import sqlite3

def test_where_vs_having():
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
        (3, 'Product C', 'Category 2', 300),
        (4, 'Product D', 'Category 2', 400)
    ]
    cursor.executemany('INSERT INTO Sales VALUES (?, ?, ?, ?)', sales)

    # Query using WHERE
    where_query = '''
    SELECT *
    FROM Sales
    WHERE category = 'Category 1';
    '''
    cursor.execute(where_query)
    print("WHERE Query Result:")
    for row in cursor.fetchall():
        print(row)

    # Query using HAVING
    having_query = '''
    SELECT category, SUM(amount) AS total_sales
    FROM Sales
    GROUP BY category
    HAVING SUM(amount) > 300;
    '''
    cursor.execute(having_query)
    print("\nHAVING Query Result:")
    for row in cursor.fetchall():
        print(row)

    # Close the connection
    conn.close()

if __name__ == '__main__':
    test_where_vs_having()
```

### How to Run
1. Copy the script into a Python file (e.g., `where_vs_having.py`).
2. Run the script using Python.
3. Verify the output matches the expected results.

---

Happy Learning 🚀