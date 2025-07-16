
with source as (
    select
        id as message_id,
        channel as channel_id,
        text,
        date,
        sender_id,
        has_photo as contains_media,
        media_file
    from {{ source('raw', 'messages') }}
)

select
    message_id,
    channel_id,
    text,
    date,
    sender_id,
    contains_media,
    media_file
from source
where text is not null
