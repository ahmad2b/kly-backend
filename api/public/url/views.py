from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session
from typing import Annotated, Any

from api.database import get_session
from api.auth import get_current_user_optional

from api.utils.errors import Duplicate
from api.utils.logger import logger_config

from api.public.url import crud as service
from api.public.url.models import URL, UrlRequest


router = APIRouter()
logger = logger_config(__name__)


@router.post(
    "",
    tags=["URL"],
    response_model=URL,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    db: Annotated[Session, Depends(get_session)],
    url: UrlRequest,
    user: Annotated[Any | None, Depends(get_current_user_optional)] = None,
) -> URL:
    try:
        if not user:
            logger.info("Creating URL without user_id", extra={"url": url.url})
            updated_url = URL(
                url=str(url.url), short_url=url.short_url, user_id=url.user_id
            )
        else:
            logger.info(
                "Creating URL with user_id",
                extra={"user_id": user["user_id"], "url": url.url},
            )
            updated_url = URL(
                url=str(url.url), short_url=url.short_url, user_id=user["user_id"]
            )

        return service.create(db, updated_url)
    except Duplicate as e:
        logger.error("Duplicate URL", extra={"url": url.url})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        logger.error("Invalid URL", extra={"url": url.url})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/{short_url}",
    tags=["URL"],
    description="Retrieves the original URL for a given short URL. If the short URL does not exist in the database, an error will be returned.",
    responses={
        400: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Short URL does not exist",
                    }
                }
            }
        },
    },
    deprecated=False,
)
async def get_original_url(
    short_url: str,
    db: Session = Depends(get_session),
):
    try:
        url = service.get_url(db, short_url)
        if not url:
            logger.error("Short URL does not exist", extra={"short_url": short_url})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Short URL does not exist"
            )
        return url.url
    except Exception as e:
        logger.error("Failed to retrieve original URL", extra={"short_url": short_url})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{short_url}",
    tags=["URL"],
    description="Deletes a given short URL from the database. If the short URL does not exist, an error will be returned.",
    responses={
        400: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Short URL does not exist",
                    }
                }
            }
        },
    },
    deprecated=False,
)
async def delete_url(short_url: str, db: Session = Depends(get_session)):
    try:
        url = service.delete(db, short_url)
        logger.info("Deleted URL", extra={"short_url": short_url})
        return url
    except Exception as e:
        logger.error("Failed to delete URL", extra={"short_url": short_url})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
