from fastapi import Depends
from sqlmodel import Session, select
from typing import Optional, Annotated

from api.database import get_session
from api.public.url.models import URL
from api.utils.logger import logger_config

logger = logger_config(__name__)


def create(db: Annotated[Session, Depends(get_session)], url: URL) -> URL:
    logger.info("Creating new URL", extra={"url": url.dict()})
    db.add(url)
    db.commit()
    db.refresh(url)
    logger.info("URL created successfully", extra={"short_url": url.short_url})
    return url


def get_url(
    db: Annotated[Session, Depends(get_session)], short_url: str
) -> Optional[URL]:
    logger.info("Getting URL by short URL", extra={"short_url": short_url})
    db_url = db.exec(select(URL).where(URL.short_url == short_url)).first()
    if db_url:
        logger.info("URL found", extra={"url": db_url.dict()})
    else:
        logger.info("URL not found", extra={"short_url": short_url})
    return db_url


def delete(
    db: Annotated[Session, Depends(get_session)], short_url: str
) -> Optional[URL]:
    logger.info("Deleting URL by short URL", extra={"short_url": short_url})
    db_url = db.exec(select(URL).where(URL.short_url == short_url)).first()
    if db_url:
        db.delete(db_url)
        db.commit()
        logger.info("URL deleted", extra={"url": db_url.dict()})
        return db_url
    else:
        logger.info("URL not found", extra={"short_url": short_url})
        return None
