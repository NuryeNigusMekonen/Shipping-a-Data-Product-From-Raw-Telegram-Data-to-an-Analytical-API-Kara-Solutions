{{ config(materialized='table') }}

SELECT
    id AS message_id,
    channel_name,
    message_date::date AS date,
    sender_id,
    has_photo,
    message_length,
    text
FROM {{ ref('stg_telegram_messages') }}
