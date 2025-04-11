WITH cte AS (
    SELECT * FROM schema1.table1
)
SELECT * FROM public.table2 JOIN cte ON cte.id = table2.id