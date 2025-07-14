import json
import os
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Constants
DATA_DIR = Path("data/raw/telegram_messages")

def main():
    try:
        # Connect to PostgreSQL using environment variables
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()
        print("Connected to database.")

        # Create schema and table (drop existing with CASCADE)
        cur.execute("""
            CREATE SCHEMA IF NOT EXISTS raw;
            DROP TABLE IF EXISTS raw.messages CASCADE;
            CREATE TABLE raw.messages (
                id INTEGER PRIMARY KEY,
                channel TEXT,
                date TIMESTAMP,
                sender_id TEXT,
                text TEXT,
                has_photo BOOLEAN,
                media_file TEXT
            );
        """)
        print("Schema and table ready.")

        # Recursively load all JSON files in DATA_DIR
        json_files = list(DATA_DIR.rglob("*.json"))
        print(f"Found {len(json_files)} JSON files to process.")

        for file in json_files:
            channel_name = file.stem  # Use filename without extension as channel name
            with open(file, 'r', encoding='utf-8') as f:
                messages = json.load(f)
                for msg in messages:
                    cur.execute("""
                        INSERT INTO raw.messages (id, channel, date, sender_id, text, has_photo, media_file)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                    """, (
                        msg.get("id"),
                        channel_name,  # <-- Updated here
                        msg.get("date"),
                        msg.get("sender_id"),
                        msg.get("text"),
                        msg.get("has_photo"),
                        msg.get("media_file")
                    ))
            print(f"Inserted messages from {file}")

        conn.commit()
        print("All data inserted successfully.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            cur.close()
            conn.close()
            print("Database connection closed.")
        except:
            pass

if __name__ == "__main__":
    main()
