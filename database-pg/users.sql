-- Create Users Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL, -- Store hashed passwords securely
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	delete_requested BOOLEAN DEFAULT FALSE
);

-- Trigger for auto-updating updated_at
CREATE OR REPLACE FUNCTION update_users_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_timestamp_trigger
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_users_timestamp();

-- Index on email for faster lookups
CREATE INDEX idx_email ON users (email);

-- Seed Data
INSERT INTO users (first_name, last_name, email, password_hash)
VALUES 
('Alice', 'Johnson', 'alice@example.com', 'hashed_password1'),
('Bob', 'Smith', 'bob@example.com', 'hashed_password2');