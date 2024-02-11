from fastapi import Depends
from sqlmodel import Session, select
from typing import Optional, Annotated

from api.database import get_session
from api.public.url.models import URL
from api.utils.logger import logger_config

logger = logger_config(__name__)


def create(db: Annotated[Session, Depends(get_session)], url: URL) -> URL:
    logger.info(f"Creating new URL. Details: {url}")
    db.add(url)
    db.commit()
    db.refresh(url)
    logger.info(f"URL created successfully. Short_url: {url.short_url}")
    return url


def get_url(
    db: Annotated[Session, Depends(get_session)], short_url: str
) -> Optional[URL]:
    logger.info(f"Getting URL by short URL: {short_url}")
    db_url = db.exec(select(URL).where(URL.short_url == short_url)).first()
    logger.info(f"URL found: {db_url}")
    return db_url


def delete(
    db: Annotated[Session, Depends(get_session)], short_url: str
) -> Optional[URL]:
    logger.info(f"Deleting URL by short URL: {short_url}")
    db_url = db.exec(select(URL).where(URL.short_url == short_url)).first()
    if db_url:
        db.delete(db_url)
        db.commit()
        logger.info(f"URL deleted: {db_url}")
        return db_url
    else:
        logger.info(f"URL not found: {short_url}")
        return None
