from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file from root

DATABASE_URL = os.getenv("DATABASE_URL")  # e.g. "postgresql+psycopg2://user:password@host:port/dbname"

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Use scoped_session if you want thread safety (e.g. for async or multi-thread)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_db():
    """
    FastAPI dependency to provide DB session and ensure it is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
