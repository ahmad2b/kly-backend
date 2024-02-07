import requests
from typing import Optional
from datetime import datetime, timezone
from jose import JWTError, jwt, jwk

from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from api.config import settings
from api.public.user.models import UserCreate, UserSignupResponse
from api.utils.errors import (
    HTTPError,
    BadRequest,
    NotFound,
    Unauthorized,
    Forbidden,
    UnprocessableEntity,
    OK,
)
from api.utils.logger import logger_config
from api.auth.model import Token


logger = logger_config(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Clerk:
    def __init__(self):
        self.CLERK_BACKEND_API_URL = settings.CLERK_BACKEND_API_URL
        self.token = settings.CLERK_SECRET_KEY
        self.CLERK_FRONTEND_API_URL = settings.CLERK_FRONTEND_API_URL
        self.CLERK_JWKS_URL = settings.CLERK_JWKS_URL

    def retrieve_user_information(self, user_id: str):
        logger.info(
            f"Attempting to retrieve user information from Clerk for user_id: {user_id}"
        )
        response = requests.get(
            f"{self.CLERK_BACKEND_API_URL}/users/{user_id}",
            headers={
                "Authorization": f"Bearer {self.token}",
            },
        )

        if response.status_code == 200:
            logger.info(
                f"Successfully retrieved user information from Clerk for user_id: {user_id}"
            )
            data = response.json()
            return {
                "email_address": data["email_addresses"][0]["email_address"],
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "last_login": datetime.fromtimestamp(
                    data["last_sign_in_at"] / 1000, tz=datetime.now(timezone.utc).tzinfo
                ),
            }, True
        else:
            logger.error(
                f"Failed to retrieve user information from Clerk for user_id: {user_id}. Error message: {response.text}"
            )
            return {
                "email_address": "",
                "first_name": "",
                "last_name": "",
                "last_login": None,
            }, False

    def fetch_json_web_key_set(self):
        logger.info("Attempting to fetch JWKS.")
        # jwks_data = cache.get(CACHE_KEY)
        # if not jwks_data:
        logger.info("JWKS not found in cache. Fetching from Clerk.")
        response = requests.get(f"{self.CLERK_JWKS_URL}")
        if response.status_code == 200:
            logger.info("Successfully fetched JWKS from Clerk.")
            jwks_data = response.json()
            # cache.set(CACHE_KEY, jwks_data)  # cache indefinitely
        else:
            logger.info(
                f"Failed to fetch JWKS from Clerk. Error message: {response.text}"
            )
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to fetch JWKS from Clerk. Error message: {response.text}",
                headers={"Content-Type": "application/json"},
            )
        return jwks_data

    def register_new_user(self, user: UserCreate) -> Optional[UserSignupResponse]:
        user_data = {
            "email_address": [f"{user.email_address}"],
            "username": f"{user.username}",
            "password": f"{user.password}",
            "skip_password_checks": True,
            "skip_password_requirement": False,
            "created_at": f"{datetime.now(timezone.utc).isoformat()}",
        }
        logger.info(f"Registering new user with data: {user_data}")

        try:
            response = requests.post(
                f"{self.CLERK_BACKEND_API_URL}/users",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                },
                json=user_data,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            logger.error(
                f"HTTP {response.status_code} Error occurred registering user. Error message: {http_err}",
            )
            raise HTTPError(
                response.status_code,
                f"HTTP ({response.status_code}) Error occurred registering user. Error message: {http_err}",
            )
        except requests.exceptions.RequestException as err:
            logger.error(
                f"Request Exception: An error occurred during the request: {err}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Request Exception: An error occurred during the request: {err}",
            )
        except Exception as err:
            logger.error(f"Unexpected Exception: An unexpected error occurred: {err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected Exception: An unexpected error occurred: {err}",
            )
        else:
            logger.info("Successfully registered user.")
            data = response.json()
            return data

    def authenticate_and_obtain_token(self, user: UserCreate) -> Token:
        logger.info(
            "Attempting to authenticate user with details: %s", user.email_address
        )
        data = {
            "strategy": "password",
            "identifier": f"{user.username}",
            "password": f"{user.password}",
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {self.token}",
        }

        try:
            response = requests.post(
                f"{self.CLERK_FRONTEND_API_URL}/v1/client/sign_ins",
                headers=headers,
                data=data,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            logger.error(
                f"HTTP {response.status_code} Error occurred during user authentication. Error message: {http_err}",
            )
            raise HTTPError(
                response.status_code,
                f"HTTP ({response.status_code}) Error occurred during user authentication. Error message: {http_err}",
            )
        except requests.exceptions.RequestException as err:
            logger.error(
                f"Request Exception: An error occurred during the request: {err}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Request Exception: An error occurred during the request: {err}",
            )
        except Exception as err:
            logger.error(f"Unexpected Exception: An unexpected error occurred: {err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected Exception: An unexpected error occurred: {err}",
            )
        else:
            logger.info("Successfully authenticated user.")
            data = response.json()
            jwt = self.fetch_jwt_token(data["client"]["sessions"][0]["id"])  # type: ignore
            return jwt

    def fetch_jwt_token(self, user_session: str):
        logger.info(f"Attempting to fetch JWT token for user session: {user_session}")
        response = requests.post(
            f"{self.CLERK_BACKEND_API_URL}/sessions/{user_session}/tokens/kly_test_jwt",
            headers={
                "Authorization": f"Bearer {self.token}",
            },
        )
        if response.status_code == 200:
            logger.info("Successfully fetched JWT token.")
            data = response.json()
            return data
        else:
            logger.error(
                f"Failed to fetch JWT token. Error message: {response.status_code} {response.json()}"
            )
            return None


class JWTAuthentication:
    def __init__(self, token: str = Depends(oauth2_scheme)):
        self.token = token

    def authenticate_user_token(self):
        logger.info(f"Attempting to authenticate user token: {self.token}")
        try:
            token = self.token
        except IndexError:
            logger.error("Bearer token not provided.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bearer token not provided.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = self.decode_jwt_token(token)
        clerk = Clerk()
        logger.info(f"User: {user}")
        info, found = clerk.retrieve_user_information(user)
        if not user:
            return None
        # else:
        #     if found:
        #         user.email = info["email_address"]
        #         user.first_name = info["first_name"]
        #         user.last_name = info["last_name"]
        #         user.last_login = info["last_login"]
        #     user.save()
        logger.info(f"Successfully authenticated user token for user: {user}")
        return user, None

    def get_public_key(jwks_url, token_kid):
        jwks = requests.get(jwks_url).json()
        key = next((key for key in jwks["keys"] if key["kid"] == token_kid), None)
        if key:
            return jwt.jwk.construct(key)
        return None

    def decode_jwt_token(self, token: str):
        clerk = Clerk()
        jwks_data = clerk.fetch_json_web_key_set()

        # public_key = ALGORITHMS.RSA.from_jwk(jwks_data["keys"][0])
        # ----

        headers = jwt.get_unverified_headers(token)
        kid = headers["kid"]
        key_index = next(
            (index for (index, d) in enumerate(jwks_data["keys"]) if d["kid"] == kid),
            None,
        )

        if key_index is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Public key not found.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        public_key = jwk.construct(jwks_data["keys"][key_index])

        # ----
        try:
            payload = jwt.decode(
                # token,
                # public_key,
                # algorithms=["RS256"],
                # options={"verify_signature": False},
                token,
                public_key.to_pem(),
                algorithms=["RS256"],
            )
        except JWTError as e:
            error_message = str(e)
            if "Signature has expired" in error_message:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            elif "Error decoding signature" in error_message:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token decode error.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token.",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id


def get_current_user(token: str = Depends(oauth2_scheme)):
    logger.info(f"Attempting to get current user with token")
    jwt_auth = JWTAuthentication(token)
    user, _ = jwt_auth.authenticate_user_token()
    if not user:
        logger.error(f"Invalid authentication credentials")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.info(f"Successfully retrieved current user with token")
    return user
