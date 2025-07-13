{{ config(materialized='table') }}

select
    id,
    channel as channel_name,
    date::timestamp as message_date,
    sender_id,
    text,
    has_photo,
    media_file
from {{ source('raw', 'messages') }}
