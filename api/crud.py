from sqlalchemy.orm import Session
from sqlalchemy import text
import datetime

def get_top_products(db: Session, limit: int = 10):
    print(" Running UPDATED get_top_products()")
    query = text("""
        SELECT channel_name, COUNT(*) AS mention_count
        FROM raw.fct_messages
        GROUP BY channel_name
        ORDER BY mention_count DESC
        LIMIT :limit;
    """)
    result = db.execute(query, {"limit": limit})
    rows = result.fetchall()
    print(" SQL Output:", rows)
    return [{"product_name": row[0], "mention_count": row[1]} for row in rows]


# Similarly for other queries:
def get_channel_activity(db: Session, channel_name: str):
    query = text("""
        SELECT date, COUNT(*) AS message_count
        FROM raw.fct_messages
        WHERE channel_name = :channel_name
        GROUP BY date
        ORDER BY date;
    """)
    result = db.execute(query, {"channel_name": channel_name}).mappings()
    rows = [dict(row) for row in result]

    # Convert date field to ISO string for each row
    for row in rows:
        if isinstance(row['date'], (datetime.date, datetime.datetime)):
            row['date'] = row['date'].isoformat()  # or str(row['date'])

    return rows

from sqlalchemy.sql import text

def search_messages(db, query_text):
    query = text("""
        SELECT id AS message_id, channel_name, message_date::date AS date, sender_id, text
        FROM raw.stg_telegram_messages
        WHERE text ILIKE '%' || :query_text || '%'
        LIMIT 50;
    """)
    result = db.execute(query, {"query_text": query_text})
    return [dict(row._mapping) for row in result]  # ✅ necessary for FastAPI to serialize





