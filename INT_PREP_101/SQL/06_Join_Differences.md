# Question 6: Difference: INNER vs LEFT vs FULL JOIN (use cases)

## Explanation

Joins in SQL are used to combine rows from two or more tables based on a related column. The type of join determines which rows are included in the result set.

### Types of Joins:
1. **INNER JOIN**: Returns only the rows with matching values in both tables.
2. **LEFT JOIN**: Returns all rows from the left table and matching rows from the right table. Rows with no match in the right table will have `NULL` values.
3. **FULL JOIN**: Returns all rows from both tables. Rows with no match in either table will have `NULL` values.

### SQL Schema
Assume we have two tables, `Customers` and `Orders`:
```sql
CREATE TABLE Customers (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE Orders (
    id INT PRIMARY KEY,
    customer_id INT,
    product VARCHAR(100)
);
```

### Example Data
```sql
INSERT INTO Customers (id, name) VALUES
(1, 'Alice'),
(2, 'Bob'),
(3, 'Charlie');

INSERT INTO Orders (id, customer_id, product) VALUES
(1, 1, 'Product A'),
(2, 1, 'Product B'),
(3, 2, 'Product C');
```

### Queries

#### INNER JOIN
```sql
SELECT Customers.name, Orders.product
FROM Customers
INNER JOIN Orders
ON Customers.id = Orders.customer_id;
```
- **Use Case**: When you need only the rows with matching data in both tables.
- **Output**:
```
name    | product
-----------------
Alice   | Product A
Alice   | Product B
Bob     | Product C
```

#### LEFT JOIN
```sql
SELECT Customers.name, Orders.product
FROM Customers
LEFT JOIN Orders
ON Customers.id = Orders.customer_id;
```
- **Use Case**: When you need all rows from the left table, even if there are no matches in the right table.
- **Output**:
```
name    | product
-----------------
Alice   | Product A
Alice   | Product B
Bob     | Product C
Charlie | NULL
```

#### FULL JOIN
```sql
SELECT Customers.name, Orders.product
FROM Customers
FULL JOIN Orders
ON Customers.id = Orders.customer_id;
```
- **Use Case**: When you need all rows from both tables, including unmatched rows.
- **Output**:
```
name    | product
-----------------
Alice   | Product A
Alice   | Product B
Bob     | Product C
Charlie | NULL
NULL    | Product D
```
(Note: SQLite does not support FULL JOIN directly. You can simulate it using `UNION`.)

---

## Testable Code Module

### Python Script to Test the Queries
Below is a Python script using SQLite to test the queries:

```python
import sqlite3

def test_joins():
    # Connect to SQLite database (or create in-memory database)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Create Customers and Orders tables
    cursor.execute('''
    CREATE TABLE Customers (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE Orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product TEXT
    );
    ''')

    # Insert example data
    customers = [
        (1, 'Alice'),
        (2, 'Bob'),
        (3, 'Charlie')
    ]
    orders = [
        (1, 1, 'Product A'),
        (2, 1, 'Product B'),
        (3, 2, 'Product C')
    ]
    cursor.executemany('INSERT INTO Customers VALUES (?, ?)', customers)
    cursor.executemany('INSERT INTO Orders VALUES (?, ?, ?)', orders)

    # INNER JOIN
    print("INNER JOIN Results:")
    inner_join_query = '''
    SELECT Customers.name, Orders.product
    FROM Customers
    INNER JOIN Orders
    ON Customers.id = Orders.customer_id;
    '''
    cursor.execute(inner_join_query)
    for row in cursor.fetchall():
        print(row)

    # LEFT JOIN
    print("\nLEFT JOIN Results:")
    left_join_query = '''
    SELECT Customers.name, Orders.product
    FROM Customers
    LEFT JOIN Orders
    ON Customers.id = Orders.customer_id;
    '''
    cursor.execute(left_join_query)
    for row in cursor.fetchall():
        print(row)

    # FULL JOIN (Simulated using UNION)
    print("\nFULL JOIN Results:")
    full_join_query = '''
    SELECT Customers.name, Orders.product
    FROM Customers
    LEFT JOIN Orders
    ON Customers.id = Orders.customer_id
    UNION
    SELECT Customers.name, Orders.product
    FROM Orders
    LEFT JOIN Customers
    ON Customers.id = Orders.customer_id;
    '''
    cursor.execute(full_join_query)
    for row in cursor.fetchall():
        print(row)

    # Close the connection
    conn.close()

if __name__ == '__main__':
    test_joins()
```

### How to Run
1. Copy the script into a Python file (e.g., `test_joins.py`).
2. Run the script using Python.
3. Verify the output matches the expected results.

---

Happy Learning 🚀