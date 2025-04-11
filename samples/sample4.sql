WITH cte1 AS (
    SELECT * FROM table1
),
cte2 AS (
    SELECT * FROM table2
),
cte3 AS (
    SELECT * FROM cte1 JOIN table3 ON cte1.id = table3.id
)
SELECT * FROM cte2 JOIN cte3 ON cte2.id = cte3.id