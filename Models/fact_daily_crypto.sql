{{ config(
    materialized='table',
    schema='gold'
) }}

{{ config(
    materialized='table',
    schema='gold'
) }}

WITH silver_data AS (
    SELECT * FROM {{ ref('crypto_market_cleaned') }}
),


market_totals AS (
    SELECT 
        record_timestamp,
        SUM(market_cap_usd) AS total_market_cap
    FROM silver_data
    GROUP BY record_timestamp
)

SELECT 
    s.surrogate_key,
    s.id,
    s.coin_symbol,
    s.coin_name,
    s.price_usd,
    s.market_cap_usd,
    s.total_volume_24h,

    ROUND((s.market_cap_usd / NULLIF(m.total_market_cap, 0)) * 100, 2) AS market_dominance_percentage,
    s.record_timestamp
FROM silver_data s
JOIN market_totals m ON s.record_timestamp = m.record_timestamp