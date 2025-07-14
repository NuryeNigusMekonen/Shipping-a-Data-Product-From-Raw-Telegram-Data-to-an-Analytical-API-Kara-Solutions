{{ config(materialized='view') }}

SELECT
    id,
    channel AS channel_name,
    CAST(date AS TIMESTAMP) AS message_date,
    sender_id,

    -- Aggressively clean text
    regexp_replace(
        regexp_replace(
            regexp_replace(
                regexp_replace(
                    regexp_replace(
                        regexp_replace(
                            regexp_replace(
                                text,
                                '[\n\r\t]+', ' ', 'g'           -- Remove line breaks and tabs
                            ),
                            '\s+', ' ', 'g'                    -- Collapse extra spaces
                        ),
                        '(https?:\/\/[^\s]+)', '', 'g'         -- Remove URLs
                    ),
                    '(\+251[0-9]+)', '', 'g'                   -- Remove phone numbers
                ),
                '[#@💉✅🔴🔥➡️🧿📞📆📦⏳💊☎️📲📌🔔🎉🌟✨🚒⛑️🎁🔬👩‍⚕️]+', '', 'g'  -- Remove emojis and symbols
            ),
            '[^[:print:]]', '', 'g'                            -- Remove non-printable characters
        ),
        '(?i)(DM at|Updates|importNitsihit|tikvah_sales|e_Pharma1)', '', 'g' -- Remove residual tags
    ) AS text,

    has_photo,
    media_file,
    LENGTH(text) AS message_length
FROM {{ source('raw', 'messages') }}
