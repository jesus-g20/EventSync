-- Create Payments Table
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    cart_id INT NOT NULL REFERENCES carts(cart_id),
    amount DECIMAL(10, 2) NOT NULL CHECK (amount > 0), -- Ensure valid amounts
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING', -- PENDING, COMPLETED, or FAILED
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for querying by status
CREATE INDEX idx_payment_status ON payments (status);

-- Seed Data
INSERT INTO payments (user_id, cart_id, amount, status)
VALUES 
(1, 1, 49.99, 'COMPLETED'),
(2, 2, 19.99, 'PENDING');
