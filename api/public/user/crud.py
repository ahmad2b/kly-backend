from fastapi import Depends, HTTPException, status

from api.public.user.models import UserCreate, UserSignupResponse
from api.public.user.models import User
from api.database import get_session
from api.utils.errors import Missing
from sqlmodel import Session
from api.utils.logger import logger_config

logger = logger_config(__name__)


def create_user(user, db: Session = Depends(get_session)) -> User:
    logger.info("Attempting to create a new user with details: %s", user)

    db_user = User(
        id=user["id"],
        username=user["username"],
        email_address=user["email_addresses"][0]["email_address"],
        created_at=user["created_at"],
    )
    validated = User.validate(db_user)
    db.add(validated)
    db.commit()
    db.refresh(validated)
    logger.info("Successfully created a new user with ID: %s", validated.id)
    return validated


def get_user(user_id: str, db: Session = Depends(get_session)) -> User:
    logger.info("Attempting to retrieve user with ID: %s", user_id)

    user = db.get(User, user_id)
    if not user:
        logger.error("Failed to retrieve user. User with ID: %s not found", user_id)
        raise Missing(
            f"Failed to retrieve user. User with ID: {user_id} not found in the database."
        )
    logger.info("Successfully retrieved user with ID: %s", user_id)
    return user


def get_user_by_username(username: str, db: Session = Depends(get_session)) -> User:
    logger.info("Attempting to retrieve user with username: %s", username)

    user = db.get(User, username)
    if not user:
        logger.error(
            "Failed to retrieve user. User with username: %s not found", username
        )
        raise Missing(
            f"Failed to retrieve user. User with username: {username} not found in the database."
        )
    logger.info("Successfully retrieved user with username: %s", username)
    return user
