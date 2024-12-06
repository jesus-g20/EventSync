-- Create Audit Logs Table
CREATE TABLE audit_logs (
    log_id SERIAL PRIMARY KEY,
    action_type VARCHAR(50) NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    old_data JSONB,
    new_data JSONB,
    action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger to log changes to users
CREATE OR REPLACE FUNCTION log_user_changes()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_logs (action_type, table_name, old_data, new_data)
    VALUES (
        TG_OP,
        'users',
        row_to_json(OLD),
        row_to_json(NEW)
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER log_user_changes_trigger
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW
EXECUTE FUNCTION log_user_changes();
