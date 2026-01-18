# SQL & Python — Practical and Conceptual Answers ✅

## SQL (Practical First)

### Problem
Tables:
- `products (product_id, product_name, price)`
- `sales (sales_id, product_id, quantity)`

### Query — total revenue per product
```sql
SELECT
  p.product_id,
  p.product_name,
  SUM(s.quantity * p.price) AS total_revenue
FROM products p
LEFT JOIN sales s
  ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_revenue DESC;
```

#### What I did in the query
- Joined `products` with `sales` on `product_id` to bring price and quantity together.
- Multiplied `quantity * price` per sale to compute revenue per sale row.
- Aggregated with `SUM(...)` grouped by product to get total revenue for each product.
- Used `LEFT JOIN` so products with zero sales still appear (with NULL quantities treated as 0 by aggregation).

#### Join and aggregation explanation
- Join: `LEFT JOIN sales s ON p.product_id = s.product_id` pairs each product row with its matching sales rows. If a product has no sales, `s.*` will be NULL but the product still appears (Left join semantics).
- Aggregation: `SUM(s.quantity * p.price)` computes the total revenue by summing revenue contributions from each sale row per product. `GROUP BY p.product_id, p.product_name` ensures one aggregated row per product.

---

## SQL (Conceptual)

### What is a CTE?
A Common Table Expression (CTE) is a named temporary result set defined using `WITH ... AS (...)` that can be referenced within a SQL statement (typically a `SELECT`, `INSERT`, `UPDATE`, or `DELETE`).

### Why do we use CTEs?
- Improve readability by breaking complex queries into named building blocks.
- Allow for logical separation of steps (e.g., filter, aggregate, then join).
- Support recursion (recursive CTEs) for hierarchical queries.
- Can simplify debugging and maintenance.

Example:
```sql
WITH recent_sales AS (
  SELECT product_id, SUM(quantity) qty
  FROM sales
  WHERE sale_date >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY product_id
)
SELECT p.product_name, rs.qty
FROM products p
JOIN recent_sales rs ON p.product_id = rs.product_id;
```

### Difference between UNION and UNION ALL
- `UNION` deduplicates results (performs implicit `DISTINCT`) — may incur a sort or hash step.
- `UNION ALL` concatenates results **without** deduplication — faster if duplicates are acceptable.

### How do NULL values behave in SQL?
- `NULL` means unknown/missing. Comparisons with `NULL` (e.g., `= NULL`) are unknown; use `IS NULL` / `IS NOT NULL`.
- Aggregate functions: `SUM`, `COUNT`, `AVG` ignore `NULL` values (but `COUNT(*)` counts rows regardless).
- `NULL` in expressions usually yields `NULL` (e.g., `NULL + 5` is `NULL`). Use `COALESCE` or `IFNULL` to substitute a default.

---

## Python (Programming Question)

Below example uses pandas to read a CSV, display rows, drop duplicates, and drop nulls. You can adapt reading to other formats using `pd.read_excel`, `pd.read_json`, etc.

```python
import pandas as pd

# Read CSV (change path to your file)
df = pd.read_csv('data/my_data.csv')

# Display rows
print(df.head(10))  # first 10 rows

# Remove duplicate records (keeps first occurrence by default)
df_no_dupes = df.drop_duplicates()

# Remove rows with any null values
df_no_nulls = df_no_dupes.dropna()

# Or: remove rows where certain columns are null
df_filtered = df_no_dupes.dropna(subset=['important_col1', 'important_col2'])

# Show resulting counts
print('Original rows:', len(df))
print('After dedupe:', len(df_no_dupes))
print('After removing nulls:', len(df_no_nulls))
```

Notes:
- For large files, use `chunksize` in `pd.read_csv(..., chunksize=...)` to iterate and process with less memory.
- You can fill nulls instead of dropping: `df.fillna({'col': default_value})`.

---

## Python (Conceptual)

### How do you use Python in your current work?
- I use Python for data ingestion, ETL pipelines, data cleaning, feature engineering, analysis, automation scripts, and building small services or CLI tools. I rely on libraries like `pandas`, `sqlalchemy`, `requests`, and `pytest` for testing.

### How do you manage version control for Python scripts?
- Use `git` for source control, with feature branches, code reviews (pull requests), descriptive commit messages, and CI checks (linters, unit tests). Use semantic versioning for packaged projects and pin dependencies via `requirements.txt` or `Pipfile`/`poetry`.

### Difference between list and tuple
- `list`: mutable (can append, modify), defined with `[]`. Use when data will change.
- `tuple`: immutable, defined with `()`. Use for fixed collections or as keys in dictionaries when appropriate. Tuples can be slightly faster and safer when immutability is desired.

### How do you handle Python code changes while working in a team?
- Workflow: create feature branch → write code & tests → run linter & unit tests → open pull request → request reviews → CI runs tests/linting → merge after approvals.
- Use pre-commit hooks (e.g., `black`, `flake8`) and branch protection rules to maintain code quality.

---

## Behavioural — Uncertain Issue in a Data Pipeline (detailed scenario)

### Scenario
You're operating an ETL pipeline that loads daily sales data from a streaming source into a warehouse. One morning, downstream dashboards show suddenly reduced totals for a major product category.

### Investigation & handling steps
1. **Observe & gather telemetry** 🔎
   - Check pipeline monitoring (job status, lag, error logs, throughput metrics).
   - Identify which job stage shows anomalies (ingest, transform, load).
2. **Reproduce the issue** 🧪
   - Run the failing pipeline step locally or on a staging environment using the same input range to see if the error is deterministic.
3. **Look at recent changes** 🧾
   - Check recent commits, infra changes, and schema updates (PRs merged in the last deployment window).
4. **Validate input data** 📄
   - Verify incoming files/records for schema drift, missing fields, or unexpected NULLs (use quick SQL queries or head checks).
5. **Rollback or patch** 🔧
   - If a recent change is the cause, revert or apply a hotfix (e.g., adjust parsing to handle new null pattern).
6. **Add automated checks & alerts** ⚠️
   - Add assertions or data quality tests (row counts, null thresholds, range checks) so future divergences trigger alerts earlier.
7. **Post-mortem & documentation** 📝
   - Document root cause, fix, and follow-up tasks (improve monitoring, add test cases).

### Why automation is important in ETL pipelines
- **Fast detection**: Automated checks and alerts surface issues immediately instead of relying on manual inspection.
- **Repeatability**: Tests prevent regressions and ensure transformations produce expected outputs across releases.
- **Scalability**: Automation allows pipelines to handle increased volume and complexity without linear increases in human effort.
- **Reliability**: Automated retries, idempotent jobs, and schema checks reduce the chance of silent data corruption.

---

## Additional resources & tips 💡
- Use `dbt` or similar tools for tested, versioned transformations.
- Implement data quality checks (Great Expectations, Deequ, or custom SQL/unit tests).
- Use CI for test suites and pre-merge checks to prevent regressions.

---

Files added (examples) ✅
- `HN/data/sample_sales.csv` — sample data including duplicates and NULLs.
- `HN/data/cleaned_sales.csv` — cleaned output written by the notebook (after running).
- `HN/python-cleaning-demo.ipynb` — Jupyter notebook demonstrating reading, displaying, deduplication, null handling, chunked reads, and saving cleaned CSV.
- `HN/sql_revenue_test.sql` — SQL script creating sample `products` and `sales` tables and running the revenue query; includes expected results.

How to run
1. Notebook: open `HN/python-cleaning-demo.ipynb` in Jupyter or VS Code and run cells. Requires `pandas` installed (e.g., `pip install pandas`).
2. SQL test: run the script in SQLite (`sqlite3 test.db < HN/sql_revenue_test.sql`) or adapt to your RDBMS and execute; it contains expected output in comments.

If you'd like, I can also:
- Add automated unit tests (pytest) for the Python cleaning steps.
- Add a CI workflow to run tests and linters on push.

---

*File created by GitHub Copilot (Raptor mini (Preview))*
