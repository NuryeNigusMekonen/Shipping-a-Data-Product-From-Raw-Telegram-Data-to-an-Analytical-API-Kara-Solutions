{{ config(materialized='view') }}

SELECT
    CAST(message_id AS INTEGER) AS message_id,
    detected_object_class AS object_class,
    CAST(confidence_score AS FLOAT) AS confidence_score
FROM {{ source('raw', 'image_detections') }}
