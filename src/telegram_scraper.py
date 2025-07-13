import os
import json
import logging
import asyncio
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.types import MessageMediaPhoto

# Hardcoded ROOT inside Docker
ROOT_DIR = Path("/app")
load_dotenv(dotenv_path=ROOT_DIR / ".env")

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
SESSION_NAME = "telegram_scraper_session"

CHANNELS = {
    "lobelia4cosmetics": "@lobelia4cosmetics",
    "tikvahpharma": "@tikvahpharma"
}

MAX_MESSAGES = 300
MAX_IMAGES = 100
SLEEP_BETWEEN_MSGS = 1
SLEEP_BETWEEN_CHANNELS = 10

today_str = datetime.now().strftime("%Y-%m-%d")
RAW_MSG_DIR = ROOT_DIR / f"data/raw/telegram_messages/{today_str}"
RAW_IMG_DIR = ROOT_DIR / f"data/raw/telegram_media/{today_str}"
LOG_DIR = ROOT_DIR / "logs"

RAW_MSG_DIR.mkdir(parents=True, exist_ok=True)
RAW_IMG_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

log_file = LOG_DIR / f"scrape_log_{today_str}.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def scrape_channel(name, link, client):
    logger.info(f" Scraping {name}...")
    messages = []
    img_count = 0
    img_dir = RAW_IMG_DIR / name
    img_dir.mkdir(parents=True, exist_ok=True)

    async for message in client.iter_messages(link, limit=MAX_MESSAGES):
        if message.message is None and not message.media:
            continue

        msg = {
            "id": message.id,
            "date": message.date.isoformat(),
            "sender_id": getattr(message.sender_id, "user_id", None),
            "text": message.message,
            "has_photo": bool(message.media),
            "media_file": None
        }

        if isinstance(message.media, MessageMediaPhoto) and img_count < MAX_IMAGES:
            img_path = img_dir / f"{message.id}.jpg"
            try:
                await client.download_media(message.media, file=img_path)
                msg["media_file"] = str(img_path)
                img_count += 1
            except Exception as e:
                logger.warning(f" Failed to download image: {e}")

        messages.append(msg)
        await asyncio.sleep(SLEEP_BETWEEN_MSGS)

    out_file = RAW_MSG_DIR / f"{name}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

    logger.info(f" Done {name} - {len(messages)} msgs, {img_count} images.")

async def main():
    logger.info(" Starting Telegram Scraper")
    try:
        async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
            if not await client.is_user_authorized():
                if TELEGRAM_PHONE:
                    await client.send_code_request(TELEGRAM_PHONE)
                    code = input("Enter Telegram login code: ")
                    await client.sign_in(phone=TELEGRAM_PHONE, code=code)
                else:
                    logger.error("Authorization failed: TELEGRAM_PHONE not set")
                    return

            for name, link in CHANNELS.items():
                await scrape_channel(name, link, client)
                await asyncio.sleep(SLEEP_BETWEEN_CHANNELS)
    except Exception as e:
        logger.error(f" Fatal Error in main(): {e}", exc_info=True)

def run_scraper():
    logger.info(" run_scraper() called")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except Exception as e:
        logger.error(f" run_scraper() failed: {e}", exc_info=True)
    finally:
        loop.close()
