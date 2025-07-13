from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Channel(Base):
    __tablename__ = "dim_channels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    url = Column(String, unique=True, nullable=True)

    messages = relationship("Message", back_populates="channel")

class Message(Base):
    __tablename__ = "fct_messages"
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, nullable=False)  # Telegram message ID
    channel_id = Column(Integer, ForeignKey("dim_channels.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    sender_id = Column(Integer, nullable=True)
    text = Column(Text, nullable=True)
    has_photo = Column(Boolean, default=False)
    media_file = Column(String, nullable=True)
    message_length = Column(Integer, nullable=False)

    channel = relationship("Channel", back_populates="messages")
