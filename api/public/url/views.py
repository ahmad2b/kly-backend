from fastapi import APIRouter, Depends, status, HTTPException, status

from api.utils.errors import Duplicate

from api.public.url.models import URL, URLCreate
from api.public.url import url_service
from api.utils.logger import logger_config
from api.database import get_session
from api.auth import get_current_user
from sqlmodel import Session
from typing import Annotated

router = APIRouter()
logger = logger_config(__name__)


@router.post(
    "",
    tags=["URL"],
    response_model=URL,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new short URL",
    description="Create a new URL. If description is not provided, the url content will be used to generate relvent alias.",
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
    # current_user=Depends(get_current_user),
) -> URL:
    logger.info("%s.create: %s", __name__, url)
    try:
        logger.info("Creating a new URL")
        # logger.info(f"current_user: {current_user}")
        # url.user_id = current_user
        logger.info(f"url: {url}")
        return url_service.create_url(db, url)
    except Duplicate as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{short_url}",
    tags=["URL"],
)
async def get_original_url(short_url: str, db: Session = Depends(get_session)):
    logger.info("%s.get_original_url: %s", __name__, short_url)
    try:
        url = url_service.get_url(short_url, db=db)
        return url.url
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
