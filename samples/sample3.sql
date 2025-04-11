WITH clear_data AS (
    SELECT * FROM test.fer
)
SELECT * FROM clear_data JOIN other_table ON clear_data.id = other_table.id