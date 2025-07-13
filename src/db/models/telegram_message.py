from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.db.base import Base

class TelegramMessage(Base):
    __tablename__ = "telegram_messages"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    sender_id = Column(String, nullable=True)
    text = Column(String, nullable=True)
    has_photo = Column(Boolean, default=False)
    media_file = Column(String, nullable=True)  # path to the media file if exists
