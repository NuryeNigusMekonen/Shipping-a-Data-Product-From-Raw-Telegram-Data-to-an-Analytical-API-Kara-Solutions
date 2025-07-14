import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Read detections
df = pd.read_csv("data/processed/detections.csv")
df = df[df["message_id"].notna()]  # remove rows without valid message_id
df["message_id"] = df["message_id"].astype(int)

# Connect to DB
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()

# Create table
cur.execute("""
    CREATE SCHEMA IF NOT EXISTS raw;

    DROP TABLE IF EXISTS raw.image_detections CASCADE;

    CREATE TABLE raw.image_detections (
        message_id INTEGER,
        image_path TEXT,
        detected_object_class TEXT,
        confidence_score FLOAT
    );
""")

# Insert records
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO raw.image_detections (message_id, image_path, detected_object_class, confidence_score)
        VALUES (%s, %s, %s, %s)
    """, (
        row["message_id"],
        row["image_path"],
        row["detected_object_class"],
        row["confidence_score"]
    ))

conn.commit()
cur.close()
conn.close()
print(" Inserted image detections into Postgres.")
