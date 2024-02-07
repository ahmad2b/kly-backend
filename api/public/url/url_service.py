import random
import string
from api.public.url.gemini import shorten_url
from api.public.url.crud import create, get_by_short_url
from api.public.user.models import UserCreate
from api.public.url.models import URL
from sqlmodel import Session
from fastapi import Depends
from api.database import get_session
from api.utils.logger import logger_config
from typing import Annotated

logger = logger_config(__name__)


def smart_url_generator(url: str) -> str:
    """
    Generates a smart URL for the given URL.
    """
    url = shorten_url(url)
    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=3))

    return url + "-" + random_string


def create_url(db: Annotated[Session, Depends(get_session)], user_url: URL) -> URL:
    """
    Creates a new URL.
    """
    logger.info(f"{__name__}.create_url: {user_url.url}")
    url = smart_url_generator(str(user_url.url))
    logger.info(f"Generated short url: {url}")

    # while get_by_short_url(url):
    #     logger.info(f"Short url '{url}' already exists. Generating a new one...")
    #     url = smart_url_generator(str(user_url.url))

    logger.info(f"Creating short url {url} for long url: {user_url.url}")

    return create(db, URL(url=user_url.url, short_url=url, user_id=user_url.user_id))


def get_url(url: str, db: Session):
    """
    Gets a URL by its short URL.
    """

    return get_by_short_url(url, db=db)
