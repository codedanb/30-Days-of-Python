# Question 3: Find duplicate records and delete only duplicates

## Explanation

To find and delete duplicate records in a table, we can use the `ROW_NUMBER()` window function. This function assigns a unique number to each row within a partition of data, based on a specified order. By identifying rows with duplicate values and keeping only the first occurrence, we can delete the duplicates.

### Steps:
1. Use the `ROW_NUMBER()` function to assign a unique number to each duplicate record.
2. Filter rows where the row number is greater than 1.
3. Delete the filtered rows.

### SQL Schema
Assume we have a table `Users` with the following schema:
```sql
CREATE TABLE Users (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
```

### Example Data
```sql
INSERT INTO Users (id, name, email) VALUES
(1, 'Alice', 'alice@example.com'),
(2, 'Bob', 'bob@example.com'),
(3, 'Alice', 'alice@example.com'),
(4, 'Charlie', 'charlie@example.com'),
(5, 'Alice', 'alice@example.com');
```

### Query to Find Duplicates
```sql
SELECT *
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY name, email ORDER BY id) AS row_num
    FROM Users
) subquery
WHERE row_num > 1;
```

### Query to Delete Duplicates
```sql
WITH CTE AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY name, email ORDER BY id) AS row_num
    FROM Users
)
DELETE FROM Users
WHERE id IN (
    SELECT id FROM CTE WHERE row_num > 1
);
```

### Explanation of the Queries
1. The `ROW_NUMBER()` function assigns a unique number to each row within a group of duplicates (grouped by `name` and `email`).
2. The `WHERE row_num > 1` condition filters out the first occurrence, leaving only duplicates.
3. The `DELETE` query removes the duplicates by targeting rows with `row_num > 1`.

### Output
- **Before Deletion**:
```
id | name    | email
----------------------
1  | Alice   | alice@example.com
2  | Bob     | bob@example.com
3  | Alice   | alice@example.com
4  | Charlie | charlie@example.com
5  | Alice   | alice@example.com
```

- **After Deletion**:
```
id | name    | email
----------------------
1  | Alice   | alice@example.com
2  | Bob     | bob@example.com
4  | Charlie | charlie@example.com
```

---

## Testable Code Module

### Python Script to Test the Queries
Below is a Python script using SQLite to test the queries:

```python
import sqlite3

def find_and_delete_duplicates():
    # Connect to SQLite database (or create in-memory database)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
    CREATE TABLE Users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    );
    ''')

    # Insert example data
    users = [
        (1, 'Alice', 'alice@example.com'),
        (2, 'Bob', 'bob@example.com'),
        (3, 'Alice', 'alice@example.com'),
        (4, 'Charlie', 'charlie@example.com'),
        (5, 'Alice', 'alice@example.com')
    ]
    cursor.executemany('INSERT INTO Users VALUES (?, ?, ?)', users)

    # Query to find duplicates
    find_duplicates_query = '''
    SELECT *
    FROM (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY name, email ORDER BY id) AS row_num
        FROM Users
    ) subquery
    WHERE row_num > 1;
    '''
    cursor.execute(find_duplicates_query)
    print("Duplicate Records:")
    for row in cursor.fetchall():
        print(row)

    # Query to delete duplicates
    delete_duplicates_query = '''
    WITH CTE AS (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY name, email ORDER BY id) AS row_num
        FROM Users
    )
    DELETE FROM Users
    WHERE id IN (
        SELECT id FROM CTE WHERE row_num > 1
    );
    '''
    cursor.execute(delete_duplicates_query)
    conn.commit()

    # Query to verify remaining records
    cursor.execute('SELECT * FROM Users;')
    print("\nRemaining Records:")
    for row in cursor.fetchall():
        print(row)

    # Close the connection
    conn.close()

if __name__ == '__main__':
    find_and_delete_duplicates()
```

### How to Run
1. Copy the script into a Python file (e.g., `find_delete_duplicates.py`).
2. Run the script using Python.
3. Verify the output matches the expected results.

---

Happy Learning 🚀