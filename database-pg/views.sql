-- Create View for Payment Summaries
CREATE VIEW user_payment_summary AS
SELECT 
    u.user_id, 
    u.first_name, 
    u.last_name, 
    SUM(p.amount) AS total_spent
FROM users u
JOIN payments p ON u.user_id = p.user_id
GROUP BY u.user_id;

-- Example Query
-- SELECT * FROM user_payment_summary WHERE user_id = 1;
