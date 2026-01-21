# Question 10: Normalize vs Denormalize – when & why?

## Explanation

Normalization and denormalization are two approaches to organizing data in a database. Each has its own use cases, advantages, and disadvantages.

### Normalization
Normalization is the process of organizing data to reduce redundancy and improve data integrity. It involves dividing a database into multiple related tables and defining relationships between them.

#### Key Points:
- **Goal**: Minimize redundancy and avoid anomalies (insertion, update, deletion).
- **How**: Apply normal forms (1NF, 2NF, 3NF, etc.).
- **When to Use**: When data consistency and integrity are critical, and the database is write-intensive.

#### Example:
Consider a table `Orders`:
```sql
CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    product_name VARCHAR(100),
    product_price DECIMAL(10, 2)
);
```

This table has redundancy if the same product appears in multiple orders. To normalize:
1. Create a `Customers` table:
    ```sql
    CREATE TABLE Customers (
        customer_id INT PRIMARY KEY,
        customer_name VARCHAR(100)
    );
    ```
2. Create a `Products` table:
    ```sql
    CREATE TABLE Products (
        product_id INT PRIMARY KEY,
        product_name VARCHAR(100),
        product_price DECIMAL(10, 2)
    );
    ```
3. Update the `Orders` table:
    ```sql
    CREATE TABLE Orders (
        order_id INT PRIMARY KEY,
        customer_id INT,
        product_id INT,
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    );
    ```

### Denormalization
Denormalization is the process of combining tables to reduce the complexity of queries and improve read performance. It involves introducing redundancy to optimize for specific use cases.

#### Key Points:
- **Goal**: Optimize read performance by reducing joins.
- **How**: Combine related tables into a single table.
- **When to Use**: When the database is read-intensive, and performance is more important than redundancy.

#### Example:
Instead of having separate `Orders`, `Customers`, and `Products` tables, we can combine them into a single table:
```sql
CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    product_name VARCHAR(100),
    product_price DECIMAL(10, 2)
);
```

### Comparison Table
| Feature               | Normalization                     | Denormalization                  |
|-----------------------|------------------------------------|-----------------------------------|
| **Goal**              | Reduce redundancy, ensure integrity | Optimize read performance         |
| **Data Redundancy**   | Minimal                          | High                             |
| **Performance**       | Slower reads, faster writes       | Faster reads, slower writes       |
| **Use Case**          | Write-intensive, consistent data  | Read-intensive, performance-critical |

---

## Testable Code Module

### Python Script to Demonstrate Normalization vs Denormalization
Below is a Python script using SQLite to demonstrate both approaches:

```python
import sqlite3

def demonstrate_normalization_vs_denormalization():
    # Connect to SQLite database (or create in-memory database)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Normalized Schema
    print("Creating Normalized Schema...")
    cursor.execute('''
    CREATE TABLE Customers (
        customer_id INTEGER PRIMARY KEY,
        customer_name TEXT
    );
    ''')
    cursor.execute('''
    CREATE TABLE Products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT,
        product_price DECIMAL(10, 2)
    );
    ''')
    cursor.execute('''
    CREATE TABLE Orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id INTEGER,
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    );
    ''')

    # Insert data into normalized schema
    cursor.execute("INSERT INTO Customers VALUES (1, 'Alice')")
    cursor.execute("INSERT INTO Products VALUES (1, 'Product A', 100.00)")
    cursor.execute("INSERT INTO Orders VALUES (1, 1, 1)")

    # Query normalized schema
    print("\nNormalized Data:")
    cursor.execute('''
    SELECT o.order_id, c.customer_name, p.product_name, p.product_price
    FROM Orders o
    JOIN Customers c ON o.customer_id = c.customer_id
    JOIN Products p ON o.product_id = p.product_id;
    ''')
    for row in cursor.fetchall():
        print(row)

    # Denormalized Schema
    print("\nCreating Denormalized Schema...")
    cursor.execute('''
    CREATE TABLE DenormalizedOrders (
        order_id INTEGER PRIMARY KEY,
        customer_name TEXT,
        product_name TEXT,
        product_price DECIMAL(10, 2)
    );
    ''')

    # Insert data into denormalized schema
    cursor.execute("INSERT INTO DenormalizedOrders VALUES (1, 'Alice', 'Product A', 100.00)")

    # Query denormalized schema
    print("\nDenormalized Data:")
    cursor.execute("SELECT * FROM DenormalizedOrders;")
    for row in cursor.fetchall():
        print(row)

    # Close the connection
    conn.close()

if __name__ == '__main__':
    demonstrate_normalization_vs_denormalization()
```

### How to Run
1. Copy the script into a Python file (e.g., `normalization_vs_denormalization.py`).
2. Run the script using Python.
3. Observe the differences between normalized and denormalized data.

---

Happy Learning 🚀