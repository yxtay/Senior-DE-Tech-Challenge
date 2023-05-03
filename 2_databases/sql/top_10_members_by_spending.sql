WITH top_10_members_spending AS (
    SELECT
        user_id,
        SUM(total_price) AS total_speding
    FROM
        orders
    GROUP BY
        1
    ORDER BY
        2 DESC
    LIMIT
        10
)
SELECT
    top_10.*
    users.user_name
FROM
    top_10_members_spending AS top_10
JOIN
    users
ON
    top_10.user_id = users.user_id
