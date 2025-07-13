import json
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session
from src.db.session import SessionLocal
from src.db.models import Channel, Message

RAW_DATA_DIR = Path("data/raw/telegram_messages")

def load_data():
    session: Session = SessionLocal()

    # Scan all date folders
    for date_folder in RAW_DATA_DIR.iterdir():
        if not date_folder.is_dir():
            continue

        for json_file in date_folder.glob("*.json"):
            channel_name = json_file.stem

            # Get or create channel
            channel = session.query(Channel).filter_by(name=channel_name).first()
            if not channel:
                channel = Channel(name=channel_name)
                session.add(channel)
                session.commit()

            with open(json_file, "r", encoding="utf-8") as f:
                messages = json.load(f)

            for msg in messages:
                # Convert date string to datetime
                date_obj = datetime.fromisoformat(msg["date"])

                message_length = len(msg["text"]) if msg["text"] else 0

                message = Message(
                    message_id=msg["id"],
                    channel_id=channel.id,
                    date=date_obj,
                    sender_id=msg.get("sender_id"),
                    text=msg.get("text"),
                    has_photo=msg.get("has_photo", False),
                    media_file=msg.get("media_file"),
                    message_length=message_length
                )

                session.add(message)
            session.commit()
            print(f"Loaded {len(messages)} messages for channel {channel_name} from {date_folder.name}")

    session.close()

if __name__ == "__main__":
    load_data()
