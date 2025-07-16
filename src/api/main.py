from fastapi import FastAPI, BackgroundTasks
from src.telegram_scraper import run_scraper

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "API is up"}

@app.post("/scrape/start", status_code=202)
def start_scraping(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_scraper)
    return {"status": "Scraping started"}
