-- Create the database
CREATE DATABASE IF NOT EXISTS sandwich_maker_api;
USE sandwich_maker_api;

-- Create customers table
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    address VARCHAR(255)
);

-- Create menu_items table
CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ingredients TEXT,
    price DECIMAL(10, 2) NOT NULL,
    calories INT,
    food_category VARCHAR(100)
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    tracking_number VARCHAR(20) UNIQUE NOT NULL,
    order_status VARCHAR(20) DEFAULT "pending",
    order_type VARCHAR(20) DEFAULT "takeout",
    total_price DECIMAL(10, 2) NOT NULL,
    item_id INT REFERENCES menu_items(id),
    quantity INT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Create order_details table
CREATE TABLE IF NOT EXISTS order_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    item_id INT,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- Create payments table
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    card_info VARCHAR(255) NOT NULL,
    transaction_status VARCHAR(20) NOT NULL,
    payment_type VARCHAR(50) NOT NULL,
    customer_id INT,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Create promotions table
CREATE TABLE IF NOT EXISTS promotions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    discount_percent DECIMAL(5, 2) NOT NULL,
    start_date DATE,
    end_date DATE
);

-- Create resources table
CREATE TABLE IF NOT EXISTS resources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ingredient_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    unit VARCHAR(20) NOT NULL,
    reorder_level INT
);

-- Create reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    rating INT NOT NULL,
    comment TEXT,
    review_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
