from pydantic import BaseModel
from typing import List
from typing import Optional

class ProductCount(BaseModel):
    product_name: str
    mention_count: int

class ChannelActivity(BaseModel):
    date: str    # or datetime.date
    message_count: int

from pydantic import BaseModel
from typing import Optional
from datetime import date

class Message(BaseModel):
    message_id: int
    channel_name: str
    date: date  #  was str before, change to datetime.date
    sender_id: Optional[str]
    text: str


