-- Insert customer data
INSERT INTO customers (name, email, phone_number, address)
VALUES
    ('Alex Johnson', 'ajohnson@gmail.com', '434-1234', '123 Fordham Blvd'),
    ('Sarah Smith', 'ssmith@gmail.com', '423-1234', '123 James St'),
    ('Marcus Williams', 'mwilliams@gmail.com', '234-1234', '123 Farrow Rd');

-- Insert menu items
INSERT INTO menu_items (name, ingredients, price, calories, food_category)
VALUES
    ('Cheeseburger', 'Beef, Cheese, Bun', 9.99, 800, 'Entree'),
    ('Pizza', 'Dough, Cheese, Tomato', 3.99, 300, 'Entree'),
    ('Salad', 'Lettuce, Tomato, Balsamic Dressing', 3.99, 200, 'Vegan'),
    ('French Fries', 'Potatoes, Salt', 2.99, 400, 'Side');

-- Insert orders
INSERT INTO orders (customer_id, order_date, tracking_number, order_status, total_price, item_id, quantity, order_type)
VALUES
    (1, '2024-12-01 13:00:00', '0001', 'completed', 9.99, 1, 3, 'takeout'),
    (2, '2024-12-02 13:30:00', '0002', 'pending', 3.99, 1, 1, 'dine-in');

-- Insert order details
INSERT INTO order_details (order_id, item_id, quantity)
VALUES
    (1, 1, 1), -- Cheeseburger
    (2, 1, 1); -- Pizza

-- Insert payment info
INSERT INTO payments (order_id, card_info, transaction_status, payment_type, customer_id)
VALUES
    (1, '5729358373', 'completed', 'debit card', 1),
    (2, '6928376832', 'pending', 'credit card', 2);

-- Insert promotions
INSERT INTO promotions (code,  discount_percent, start_date, end_date)
VALUES
    ('10OFF', 10.00, '2024-01-01', '2025-01-01');

-- Insert resources
INSERT INTO resources (ingredient_name, quantity, unit)
VALUES
    ('Beef', 50, 'units'),
    ('Cheese', 50, 'units'),
    ('Potatoes', 50, 'units');

-- Insert reviews
INSERT INTO reviews (customer_id, comment, rating, review_date)
VALUES
    (1, 'Burger was perfectly cooked.', 5, '2024-12-01 13:00:00'),
    (2, 'Pizza was served cold.', 2, '2024-12-02 13:30:00');
