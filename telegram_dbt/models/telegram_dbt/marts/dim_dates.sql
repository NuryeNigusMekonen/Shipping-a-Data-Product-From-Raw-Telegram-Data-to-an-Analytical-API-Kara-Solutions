-- models/telegram_dbt/marts/dim_dates.sql

with base as (
    select distinct
        date
    from {{ ref('stg_telegram_messages') }}
)

select
    date,
    extract(year from date) as year,
    extract(month from date) as month,
    extract(day from date) as day,
    to_char(date, 'Day') as weekday,
    to_char(date, 'YYYY-MM') as year_month,
    to_char(date, 'YYYY-MM-DD') as full_date
from base
order by date
