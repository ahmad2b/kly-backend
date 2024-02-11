from fastapi import APIRouter, Depends, status, HTTPException, status

from api.utils.errors import Duplicate

from api.public.url.models import URL, URLCreate
from api.public.url import service
from api.utils.logger import logger_config
from api.database import get_session
from api.auth import get_current_user, get_current_user_optional
from sqlmodel import Session
from typing import Annotated, Optional, Any

router = APIRouter()
logger = logger_config(__name__)


@router.post(
    "",
    tags=["URL"],
    response_model=URL,
    status_code=status.HTTP_201_CREATED,
    description="Creates a new URL entry. If a description is not provided, the content of the URL will be used to generate a relevant alias. If a token is provided, it will be used as the user_id for the URL entry. If the URL already exists, or if the URL is invalid, an error will be returned. The short URL created can be used like this: 'kly.lol/<short_url>'.",
    responses={
        400: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "URL is missing",
                    }
                }
            }
        },
        409: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "URL already exists",
                    }
                }
            }
        },
        422: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid URL",
                    }
                }
            }
        },
    },
    deprecated=False,
)
async def create(
    db: Annotated[Session, Depends(get_session)],
    url: URLCreate,
    token: Annotated[Any | None, Depends(get_current_user_optional)] = None,
) -> URL:
    logger.info("%s.create: %s", __name__, url)
    try:
        logger.info(f"Creating URL: {url} with token: {token}")
        if not token:
            logger.info(f"Token not found. Creating URL without user_id")
            updated_url = URLCreate(
                url=url.url, description=url.description, user_id=url.user_id
            )
            return service.create(db, updated_url)

        logger.info(f"Token found. Creating URL with user_id: {token['user_id']}")
        updated_url = URLCreate(
            url=url.url, description=url.description, user_id=token["user_id"]
        )
        return service.create(db, updated_url)
    except Duplicate as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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
async def get_original_url(short_url: str, db: Session = Depends(get_session)):
    logger.info("%s.get_original_url: %s", __name__, short_url)
    try:
        url = service.get_url(short_url, db=db)
        return url.url
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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
    logger.info("%s.delete_url: %s", __name__, short_url)
    try:
        url = service.delete(short_url, db=db)
        return url
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
