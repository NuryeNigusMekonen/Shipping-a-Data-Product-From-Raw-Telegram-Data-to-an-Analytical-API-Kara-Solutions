import os
import json
from pathlib import Path
from sqlalchemy.exc import SQLAlchemyError

from src.db.session import SessionLocal
from src.db.models import TelegramMessage 
RAW_DATA_DIR = Path("data/raw/telegram_messages")

def load_json_to_db(json_file: Path, db_session):
    with open(json_file, "r", encoding="utf-8") as f:
        messages = json.load(f)

    for msg in messages:
        try:
            new_msg = TelegramMessage(
                message_id=msg["id"],
                date=msg["date"],
                sender_id=msg["sender_id"],
                text=msg["text"],
                has_photo=msg["has_photo"],
                media_file=msg["media_file"],
                channel_name=json_file.stem,
                raw_date_folder=json_file.parent.name  # e.g. '2025-07-11'
            )
            db_session.add(new_msg)
        except Exception as e:
            print(f"Skipping message {msg['id']}: {e}")
    try:
        db_session.commit()
    except SQLAlchemyError as e:
        print(f"Error committing to DB: {e}")
        db_session.rollback()


def load_all_jsons():
    db = SessionLocal()
    try:
        for date_dir in RAW_DATA_DIR.iterdir():
            if date_dir.is_dir():
                for json_file in date_dir.glob("*.json"):
                    print(f"Loading {json_file} ...")
                    load_json_to_db(json_file, db)
    finally:
        db.close()

if __name__ == "__main__":
    load_all_jsons()
