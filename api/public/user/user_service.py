from sqlmodel import Session
from typing import Optional

from api.auth import Clerk
from api.public.user import crud as data
from api.public.user.models import UserCreate, User
from api.utils.logger import logger_config


logger = logger_config(__name__)


def create(db: Session, user: UserCreate) -> Optional[User]:
    logger.info("%s.create_user_service: %s", __name__, user)

    clerk = Clerk()
    auth_user = clerk.register_new_user(user)
    if auth_user is None:
        return None
    print(f"\n{auth_user}")

    db_user = data.create_user(auth_user, db=db)
    return db_user


def get_one(user_id: str):
    return user_id


def sign_in(db: Session, user: UserCreate):
    logger.info("%s.login_user_service: %s", __name__, user)

    clerk = Clerk()
    user_token = clerk.authenticate_and_obtain_token(user)
    if user_token is None:
        return None

    return user_token
