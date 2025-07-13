{{ config(materialized='table') }}

SELECT DISTINCT
    message_date::date AS date
FROM {{ ref('stg_telegram_messages') }}
