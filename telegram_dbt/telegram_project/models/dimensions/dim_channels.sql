{{ config(materialized='table') }}

SELECT DISTINCT
    channel_name
FROM {{ ref('stg_telegram_messages') }}
