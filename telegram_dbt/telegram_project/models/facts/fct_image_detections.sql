{{ config(materialized='table') }}

SELECT
    CAST(img.message_id AS INTEGER) AS message_id,
    img.object_class,
    img.confidence_score
FROM
    {{ ref('stg_image_detections') }} AS img
JOIN
    {{ ref('fct_messages') }} AS msg
    ON CAST(img.message_id AS INTEGER) = msg.message_id
