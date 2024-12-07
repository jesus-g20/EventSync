-- Create Carts Table
CREATE TABLE carts (
    cart_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    event_id INT NOT NULL REFERENCES events(event_id),
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0), -- Ensure positive quantity
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, event_id) -- Prevent duplicate entries in cart
);

-- Index for faster cart lookups
CREATE INDEX idx_cart_user_event ON carts (user_id, event_id);

-- Seed Data
INSERT INTO carts (user_id, event_id, quantity)
VALUES 
(1, 1, 2),
(2, 2, 1);
