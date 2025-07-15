from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from .database import get_db
from . import crud, schemas

app = FastAPI(title="Telegram Analytical API")

@app.get("/api/reports/top-products", response_model=List[schemas.ProductCount])
def top_products(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    products = crud.get_top_products(db, limit)
    return products


@app.get("/api/channels/{channel_name}/activity", response_model=List[schemas.ChannelActivity])
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    activity = crud.get_channel_activity(db, channel_name)
    if not activity:
        raise HTTPException(status_code=404, detail="Channel not found or no activity")
    return activity

@app.get("/api/search/messages", response_model=List[schemas.Message])
def search_messages(query: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    results = crud.search_messages(db, query)
    return results

@app.get("/")
def root():
    return {"message": "Telegram Analytical API is running"}
