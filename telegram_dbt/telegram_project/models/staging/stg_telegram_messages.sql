{{ config(materialized='view') }}

SELECT
    id,
    channel AS channel_name,
    CAST(date AS TIMESTAMP) AS message_date,
    sender_id,
    text,
    has_photo,
    media_file,
    LENGTH(text) AS message_length
FROM {{ source('raw', 'messages') }}
