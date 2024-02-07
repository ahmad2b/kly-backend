from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from api.database import engine, get_session
from api.public.url.models import URL
from api.utils.logger import logger_config


from typing import Optional, Annotated

logger = logger_config(__name__)


def create(db: Annotated[Session, Depends(get_session)], url: URL) -> URL:
    logger.info(f"Attempting to create a new url with details: {url}")
    db.add(url)
    db.commit()
    db.refresh(url)
    logger.info(f"Successfully created a new url with details: {url}")
    return url


def get_by_short_url(
    short_url: str, db: Session = Depends(get_session)
) -> Optional[URL]:
    db_url = db.exec(select(URL).where(URL.short_url == short_url)).first()
    logger.info("db_url: %s", db_url)
    print(f"\n\n{db_url}\n\n")
    return db_url
