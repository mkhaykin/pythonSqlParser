WITH B13 AS (
    select * from b where b.id = 1
)
SELECT * FROM sample;

SELECT * FROM (
    SELECT * FROM sample2) as s2 INNER JOIN s1 ON s1.id = s2.id;
