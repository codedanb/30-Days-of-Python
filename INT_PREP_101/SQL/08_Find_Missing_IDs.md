# Question 8: Find missing IDs in a sequence

## Explanation

To find missing IDs in a sequence, we can use a query that generates the expected sequence of IDs and compares it with the existing IDs in the table. This can be achieved using a `LEFT JOIN` or a `CTE` (Common Table Expression).

### Key Points:
- Generate the expected sequence of IDs using a recursive CTE or a numbers table.
- Use a `LEFT JOIN` to find IDs that are missing in the actual table.

### SQL Schema
Assume we have a table `Records` with the following schema:
```sql
CREATE TABLE Records (
    id INT PRIMARY KEY
);
```

### Example Data
```sql
INSERT INTO Records (id) VALUES
(1), (2), (4), (5), (7);
```

### Query to Find Missing IDs
#### Using Recursive CTE (Common Table Expression)
```sql
WITH RECURSIVE ExpectedIDs AS (
    SELECT MIN(id) AS id
    FROM Records
    UNION ALL
    SELECT id + 1
    FROM ExpectedIDs
    WHERE id < (SELECT MAX(id) FROM Records)
)
SELECT e.id AS missing_id
FROM ExpectedIDs e
LEFT JOIN Records r
ON e.id = r.id
WHERE r.id IS NULL;
```

### Explanation of the Query
1. `WITH RECURSIVE ExpectedIDs`: Generates the sequence of expected IDs from the minimum to the maximum ID in the `Records` table.
2. `LEFT JOIN Records r ON e.id = r.id`: Joins the expected IDs with the actual IDs in the `Records` table.
3. `WHERE r.id IS NULL`: Filters out IDs that exist in the `Records` table, leaving only the missing IDs.

### Output
For the example data, the output will be:
```
missing_id
----------
3
6
```

---

## Testable Code Module

### Python Script to Test the Query
Below is a Python script using SQLite to test the query:

```python
import sqlite3

def find_missing_ids():
    # Connect to SQLite database (or create in-memory database)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Create Records table
    cursor.execute('''
    CREATE TABLE Records (
        id INTEGER PRIMARY KEY
    );
    ''')

    # Insert example data
    records = [
        (1,), (2,), (4,), (5,), (7,)
    ]
    cursor.executemany('INSERT INTO Records VALUES (?)', records)

    # Query to find missing IDs
    query = '''
    WITH RECURSIVE ExpectedIDs AS (
        SELECT MIN(id) AS id
        FROM Records
        UNION ALL
        SELECT id + 1
        FROM ExpectedIDs
        WHERE id < (SELECT MAX(id) FROM Records)
    )
    SELECT e.id AS missing_id
    FROM ExpectedIDs e
    LEFT JOIN Records r
    ON e.id = r.id
    WHERE r.id IS NULL;
    '''

    cursor.execute(query)
    print("Missing IDs:")
    for row in cursor.fetchall():
        print(row[0])

    # Close the connection
    conn.close()

if __name__ == '__main__':
    find_missing_ids()
```

### How to Run
1. Copy the script into a Python file (e.g., `find_missing_ids.py`).
2. Run the script using Python.
3. Verify the output matches the expected results.

---

Happy Learning 🚀