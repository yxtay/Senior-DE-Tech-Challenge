WITH top_3_products_quantity AS (
    SELECT
        product_id,
        SUM(quantity) AS total_quantity
    FROM
        order_details
    GROUP BY
        1
    ORDER BY
        2 DESC
    LIMIT
        3
)
SELECT
    top_3.*
    products.product_name
FROM
    top_3_products_quantity AS top_3
JOIN
    products
ON
    top_3.product_id = products.product_id
