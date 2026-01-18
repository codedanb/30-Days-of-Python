-- SQL test script for revenue query
-- Creates temporary tables, inserts sample data, runs the revenue query, and shows expected output as comments

-- Drop tables if they exist (for idempotency)
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS sales;

-- Create tables
CREATE TABLE products (
  product_id INTEGER PRIMARY KEY,
  product_name TEXT,
  price NUMERIC
);

CREATE TABLE sales (
  sales_id INTEGER PRIMARY KEY,
  product_id INTEGER,
  quantity INTEGER
);

-- Insert sample data
INSERT INTO products (product_id, product_name, price) VALUES
(1, 'Widget A', 10.00),
(2, 'Widget B', 20.00),
(3, 'Widget C', 15.50),
(4, 'Widget D', 0.00);

INSERT INTO sales (sales_id, product_id, quantity) VALUES
(1001, 1, 2),
(1002, 1, 3),
(1003, 2, 1),
(1004, 2, 1),
(1005, 3, NULL),
(1006, 4, 5);

-- The revenue query
SELECT
  p.product_id,
  p.product_name,
  SUM(COALESCE(s.quantity, 0) * COALESCE(p.price, 0)) AS total_revenue
FROM products p
LEFT JOIN sales s ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_revenue DESC;

-- Expected output (product_id, product_name, total_revenue):
-- 1, Widget A, 50.00  -- (2+3)*10.00
-- 2, Widget B, 40.00  -- (1+1)*20.00
-- 4, Widget D, 0.00   -- 5*0.00
-- 3, Widget C, 0.00   -- NULL quantity treated as 0
