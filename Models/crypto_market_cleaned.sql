{{ config(
    materialized='incremental',
    schema='silver',
    unique_key='surrogate_key'
) }}

-- CTE 
WITH raw_data AS (
    SELECT 
        LOWER(id) AS id,
        UPPER(symbol) AS coin_symbol,
        name AS coin_name,
        CAST(current_price AS NUMERIC(20, 4)) AS price_usd,
        CAST(market_cap AS NUMERIC(25, 2)) AS market_cap_usd,
        CAST(total_volume AS NUMERIC(25, 2)) AS total_volume_24h,
        ingested_at::TIMESTAMP AS record_timestamp
    FROM {{ source('bronze_source', 'raw_crypto_market_data') }}
),

deduplicated_data AS (
    SELECT 
        *,
        MD5(CONCAT(id, '_', record_timestamp::text)) AS surrogate_key,
        ROW_NUMBER() OVER (PARTITION BY id, record_timestamp ORDER BY record_timestamp DESC) as row_num
    FROM raw_data
)

SELECT 
    surrogate_key,
    id,
    coin_symbol,
    coin_name,
    price_usd,
    market_cap_usd,
    total_volume_24h,
    record_timestamp
FROM deduplicated_data
WHERE row_num = 1

-- Make transform for updated 'API data'
{% if is_incremental() %}
  AND record_timestamp > (SELECT MAX(record_timestamp) FROM {{ this }})
{% endif %}