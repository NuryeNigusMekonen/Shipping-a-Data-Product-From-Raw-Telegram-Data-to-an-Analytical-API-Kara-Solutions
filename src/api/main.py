from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
import logging
from src.db.session import get_db
from src.telegram_scraper import run_scraper
from src.analytics import query_message_stats

app = FastAPI(title="Telegram Data Product API")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    return {"message": "Welcome to the Telegram Data Product API"}

@app.post("/scrape/start", status_code=202)
async def start_scraping(background_tasks: BackgroundTasks):
    try:
        logger.info(">> Received scrape/start request")
        background_tasks.add_task(run_scraper)
        logger.info(">> Scraper scheduled")
        return {"status": "Scraping started"}
    except Exception as e:
        logger.error(f"Failed to start scraper: {e}")
        raise HTTPException(status_code=500, detail="Failed to start scraper")

@app.get("/analytics/messages/stats")
def get_message_stats(db: Session = Depends(get_db)):
    """
    Retrieve aggregated analytics from the transformed messages data.
    """
    try:
        stats = query_message_stats(db)
        return stats
    except Exception as e:
        logger.error(f"Failed to fetch analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch analytics")

@app.get("/health")
def health_check():
    return {"status": "ok"}
