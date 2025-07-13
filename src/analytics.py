from sqlalchemy.orm import Session
from sqlalchemy import func, select, text

def query_message_stats(db: Session):
    """
    Example query for analytics on messages.
    Adjust table and column names as per your DBT transformed schema.
    """
    # Example raw SQL for aggregate counts
    # Suppose you have tables: fct_messages, dim_channels
    
    sql = """
    SELECT c.channel_name,
           COUNT(m.id) AS message_count,
           AVG(LENGTH(m.text)) AS avg_message_length,
           SUM(CASE WHEN m.has_photo THEN 1 ELSE 0 END) AS images_count
    FROM fct_messages m
    JOIN dim_channels c ON m.channel_id = c.id
    GROUP BY c.channel_name
    ORDER BY message_count DESC
    """

    result = db.execute(text(sql))
    rows = [dict(row) for row in result.fetchall()]
    return {"message_stats": rows}
