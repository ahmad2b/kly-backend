from sqlmodel import Session
from typing import Optional

from api.auth import Clerk
from api.public.user import crud as data
from api.utils.logger import logger_config

from api.public.user.models import UserCreate, UserCredentials


logger = logger_config(__name__)


def create(db: Session, user: UserCreate):
    logger.info("%s.create_user_service: %s", __name__, user)

    clerk = Clerk()
    auth_user = clerk.create_user(user)
    if auth_user is None:
        return None
    print(f"\n{auth_user}")

    # db_user = data.create_user(auth_user, db=db)
    return auth_user


def get_one(user_id: str):
    return user_id


def login(db: Session, user: UserCredentials):
    logger.info("%s.login_user_service: %s", __name__, user)

    clerk = Clerk()
    user_token = clerk.authenticate_user(user)
    if user_token is None:
        return None

    return user_token


# def session_end(session_id: str, user_id: str):
#     logger.info("%s.signout_user_service: %s", __name__, session_id, user_id)

#     clerk = Clerk()
#     clerk.session_end(session_id)
#     return f"User {session_id} signed out successfully."
