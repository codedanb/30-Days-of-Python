# Question 9: Count users who logged in consecutive days

## Explanation

To count users who logged in on consecutive days, we can use the `LAG()` window function. This function allows us to compare the login date of the current row with the previous row for the same user.

### Key Points:
- Use `LAG()` to get the previous login date for each user.
- Calculate the difference between the current login date and the previous login date.
- Filter rows where the difference is exactly 1 day.

### SQL Schema
Assume we have a table `Logins` with the following schema:
```sql
CREATE TABLE Logins (
    user_id INT,
    login_date DATE
);
```

### Example Data
```sql
INSERT INTO Logins (user_id, login_date) VALUES
(1, '2026-01-01'),
(1, '2026-01-02'),
(1, '2026-01-04'),
(2, '2026-01-01'),
(2, '2026-01-03'),
(2, '2026-01-04');
```

### Query to Count Consecutive Logins
```sql
WITH LoginDifferences AS (
    SELECT user_id, login_date,
           LAG(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS previous_login_date
    FROM Logins
)
SELECT user_id, COUNT(*) AS consecutive_days_count
FROM LoginDifferences
WHERE JULIANDAY(login_date) - JULIANDAY(previous_login_date) = 1
GROUP BY user_id;
```

### Explanation of the Query
1. `LAG(login_date) OVER (PARTITION BY user_id ORDER BY login_date)`: Retrieves the previous login date for each user.
2. `JULIANDAY(login_date) - JULIANDAY(previous_login_date) = 1`: Calculates the difference in days between the current login date and the previous login date, and filters rows where the difference is exactly 1 day.
3. `COUNT(*)`: Counts the number of consecutive login days for each user.

### Output
For the example data, the output will be:
```
user_id | consecutive_days_count
--------------------------------
1       | 1
2       | 0
```

---

## Testable Code Module

### Python Script to Test the Query
Below is a Python script using SQLite to test the query:

```python
import sqlite3

def count_consecutive_logins():
    # Connect to SQLite database (or create in-memory database)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Create Logins table
    cursor.execute('''
    CREATE TABLE Logins (
        user_id INTEGER,
        login_date DATE
    );
    ''')

    # Insert example data
    logins = [
        (1, '2026-01-01'),
        (1, '2026-01-02'),
        (1, '2026-01-04'),
        (2, '2026-01-01'),
        (2, '2026-01-03'),
        (2, '2026-01-04')
    ]
    cursor.executemany('INSERT INTO Logins VALUES (?, ?)', logins)

    # Query to count consecutive logins
    query = '''
    WITH LoginDifferences AS (
        SELECT user_id, login_date,
               LAG(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS previous_login_date
        FROM Logins
    )
    SELECT user_id, COUNT(*) AS consecutive_days_count
    FROM LoginDifferences
    WHERE JULIANDAY(login_date) - JULIANDAY(previous_login_date) = 1
    GROUP BY user_id;
    '''

    cursor.execute(query)
    print("Consecutive Logins Count:")
    for row in cursor.fetchall():
        print(row)

    # Close the connection
    conn.close()

if __name__ == '__main__':
    count_consecutive_logins()
```

### How to Run
1. Copy the script into a Python file (e.g., `count_consecutive_logins.py`).
2. Run the script using Python.
3. Verify the output matches the expected results.

---

Happy Learning 🚀