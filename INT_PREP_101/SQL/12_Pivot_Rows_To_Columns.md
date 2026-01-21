# Question 12: Write a query to pivot rows to columns

## Explanation

Pivoting rows to columns is a common requirement in SQL when you want to transform data from a long format to a wide format. This can be achieved using conditional aggregation or the `PIVOT` operator (if supported by the database).

### Key Points:
- **Conditional Aggregation**: Use `CASE` statements with aggregate functions to pivot rows to columns.
- **PIVOT Operator**: Some databases (e.g., SQL Server) provide a `PIVOT` operator for this purpose.

### SQL Schema
Assume we have a table `Sales` with the following schema:
```sql
CREATE TABLE Sales (
    id INT PRIMARY KEY,
    product VARCHAR(100),
    sale_date DATE,
    amount INT
);
```

### Example Data
```sql
INSERT INTO Sales (id, product, sale_date, amount) VALUES
(1, 'Product A', '2026-01-01', 100),
(2, 'Product B', '2026-01-01', 200),
(3, 'Product A', '2026-01-02', 150),
(4, 'Product B', '2026-01-02', 250);
```

### Query to Pivot Rows to Columns
#### Using Conditional Aggregation
```sql
SELECT sale_date,
       SUM(CASE WHEN product = 'Product A' THEN amount ELSE 0 END) AS product_a_sales,
       SUM(CASE WHEN product = 'Product B' THEN amount ELSE 0 END) AS product_b_sales
FROM Sales
GROUP BY sale_date;
```

### Explanation of the Query
1. `CASE WHEN product = 'Product A' THEN amount ELSE 0 END`: Filters rows for `Product A` and sums their `amount`.
2. `SUM(...)`: Aggregates the filtered amounts.
3. `GROUP BY sale_date`: Groups the data by `sale_date` to create one row per date.

### Output
For the example data, the output will be:
```
sale_date  | product_a_sales | product_b_sales
---------------------------------------------
2026-01-01 | 100            | 200
2026-01-02 | 150            | 250
```

---

## Testable Code Module

### Python Script to Test the Query
Below is a Python script using SQLite to test the query:

```python
import sqlite3

def pivot_rows_to_columns():
    # Connect to SQLite database (or create in-memory database)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Create Sales table
    cursor.execute('''
    CREATE TABLE Sales (
        id INTEGER PRIMARY KEY,
        product TEXT,
        sale_date DATE,
        amount INTEGER
    );
    ''')

    # Insert example data
    sales = [
        (1, 'Product A', '2026-01-01', 100),
        (2, 'Product B', '2026-01-01', 200),
        (3, 'Product A', '2026-01-02', 150),
        (4, 'Product B', '2026-01-02', 250)
    ]
    cursor.executemany('INSERT INTO Sales VALUES (?, ?, ?, ?)', sales)

    # Query to pivot rows to columns
    pivot_query = '''
    SELECT sale_date,
           SUM(CASE WHEN product = 'Product A' THEN amount ELSE 0 END) AS product_a_sales,
           SUM(CASE WHEN product = 'Product B' THEN amount ELSE 0 END) AS product_b_sales
    FROM Sales
    GROUP BY sale_date;
    '''

    cursor.execute(pivot_query)
    print("Pivoted Data:")
    for row in cursor.fetchall():
        print(row)

    # Close the connection
    conn.close()

if __name__ == '__main__':
    pivot_rows_to_columns()
```

### How to Run
1. Copy the script into a Python file (e.g., `pivot_rows_to_columns.py`).
2. Run the script using Python.
3. Verify the output matches the expected results.

---

Happy Learning 🚀