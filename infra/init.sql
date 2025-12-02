-- Criação das tabelas para armazenar dados processados

CREATE TABLE IF NOT EXISTS sales_summary (
    id SERIAL PRIMARY KEY,
    product_category VARCHAR(100),
    total_sales DECIMAL(15,2),
    total_quantity INTEGER,
    avg_price DECIMAL(10,2),
    sales_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customer_metrics (
    id SERIAL PRIMARY KEY,
    customer_segment VARCHAR(50),
    total_customers INTEGER,
    avg_order_value DECIMAL(10,2),
    total_revenue DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS product_performance (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(100),
    total_sold INTEGER,
    revenue DECIMAL(15,2),
    avg_rating DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);