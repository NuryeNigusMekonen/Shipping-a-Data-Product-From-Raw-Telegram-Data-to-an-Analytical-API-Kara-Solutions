select
    id,
    channel as channel_name,
    message_date::date as date,
    sender_id,
    length(text) as message_length,
    has_photo,
    media_file
from {{ ref('stg_telegram_messages') }}
