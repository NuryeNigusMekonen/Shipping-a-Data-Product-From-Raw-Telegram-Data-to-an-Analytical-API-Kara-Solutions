from src.db.base import Base
from src.db.session import engine
from src.db.models import TelegramMessage  # ensure models are imported!

def init_db():
    Base.metadata.create_all(bind=engine)
