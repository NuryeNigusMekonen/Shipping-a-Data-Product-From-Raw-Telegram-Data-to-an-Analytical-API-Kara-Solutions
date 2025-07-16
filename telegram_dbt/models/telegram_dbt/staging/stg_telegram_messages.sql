with source as (
    select * from {{ source('raw_telegram', 'messages') }}
),

enhanced as (
    select
        id as message_id,
        channel as channel_id,
        text,
        null as views,
        null as forwards,
        null as reply_count,
        has_photo as contains_media,
        date as message_date,
        length(text) as message_length
    from source
)

select * from enhanced
