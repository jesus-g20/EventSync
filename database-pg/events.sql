-- Create Events Table
CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    event_name VARCHAR(100) NOT NULL,
    description TEXT,
    event_date TIMESTAMP NOT NULL,
    created_by INT NOT NULL REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	delete_requested BOOLEAN DEFAULT FALSE,
    CONSTRAINT future_event CHECK (event_date > CURRENT_TIMESTAMP) -- Prevent past events
);

-- Trigger for auto-updating updated_at
CREATE OR REPLACE FUNCTION update_events_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for deleting events --
CREATE OR REPLACE FUNCTION delete_event_on_request()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.delete_requested = TRUE THEN
        DELETE FROM events WHERE event_id = NEW.event_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER update_events_timestamp_trigger
BEFORE UPDATE ON events
FOR EACH ROW
EXECUTE FUNCTION update_events_timestamp();

-- Index for faster queries on event_date
CREATE INDEX idx_event_date ON events (event_date);

-- Seed Data
INSERT INTO events (event_name, description, event_date, created_by)
VALUES 
('Tech Conference', 'Learn about new tech trends', '2024-12-15 09:00:00', 1),
('Music Festival', 'Enjoy live music', '2024-12-20 18:00:00', 2);
