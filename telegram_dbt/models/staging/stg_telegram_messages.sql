{{ config(materialized='view') }}

SELECT
    id::BIGINT AS message_id,
    channel_id::TEXT,
    channel_name::TEXT,
    text::TEXT,
    date::TIMESTAMP,
    views::INTEGER,
    forwards::INTEGER,
    reply_count::INTEGER,
    contains_media::BOOLEAN,
    LENGTH(text) AS message_length,
    DATE(date) AS message_date
FROM {{ source('raw', 'telegram_messages') }}
